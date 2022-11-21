import asyncio
import logging
from concurrent import futures
from decimal import Decimal, getcontext

import grpc

import SqlConnection
import atm_pb2
import atm_pb2_grpc
from atm_pb2_grpc import AtmServicer

_cleanup_coroutines = []
getcontext().prec = 19 + 4

class AtmServicer(AtmServicer):

    async def Authenticate(self, request, context):
        sql = SqlConnection.Sql()
        try:
            cur = sql.dbConnectAndExecute(
                """SELECT AuthCode from authCode inner join users u on authCode.owner_id = u.id 
                where u.id = authCode.owner_id and u.pin = ? and u.username = ?""",
                (request.pin, request.username))
            answer = cur.next()
            if answer is None:
                return atm_pb2.AuthenticateResponse(success=False, error="Wrong pin or username")
            else:
                return atm_pb2.AuthenticateResponse(success=True, AuthCode=answer[0])
        except Exception as e:
            return atm_pb2.AuthenticateResponse(success=False, error="Backend error")

    async def Balance(self, request, context):
        sql = SqlConnection.Sql()
        try:
            cur = sql.dbConnectAndExecute(
                "select balance from balances inner join authCode aC on balances.owner_id = aC.owner_id where AuthCode=?"
                , (str(request.AuthCode),))
            if cur is None:
                return atm_pb2.BalanceReply(success=False, error="Wrong AuthCode")
            else:
                answer = cur.next()
                d = Decimal(answer[0]).as_integer_ratio()
                return atm_pb2.BalanceReply(success=True, units=d[0], denomination=d[1])
        except Exception as e:
            return atm_pb2.BalanceReply(success=False, error="Backend error")

    async def Withdraw(self, request, context):
        current = await self.Balance(atm_pb2.BalanceRequest(AuthCode=request.AuthCode), context)
        sql = SqlConnection.Sql()
        money = Decimal(Decimal(request.units) / Decimal(request.denomination))
        try:
            cur = sql.dbConnectAndExecute(
                """UPDATE balances inner join authCode aC on balances.owner_id = aC.owner_id
                                        set balance =
                                        IF(balance - ?>= 0., IF(? >= 0., balance - ?, balance), balance)
                                    where AuthCode=?""",
                (money, money, money, request.AuthCode))
            after = await self.Balance(atm_pb2.BalanceRequest(AuthCode=request.AuthCode), context)
            if await after == current:
                return atm_pb2.WithdrawReply(success=False, error="Invalid input")
            else:
                return atm_pb2.WithdrawReply(success=True)
        except Exception as e:
            return atm_pb2.WithdrawReply(success=False, error="Backend error")

    async def Deposit(self, request, context):
        current = await self.Balance(atm_pb2.BalanceRequest(AuthCode=request.AuthCode), context)
        sql = SqlConnection.Sql()
        money = Decimal(Decimal(request.units) / Decimal(request.denomination))
        try:
            cur = sql.dbConnectAndExecute(
                """UPDATE balances inner join authCode aC on balances.owner_id = aC.owner_id 
                set balance = IF(?>0.0, balance + ?, balance)
                where AuthCode=?
                """,
                (money, money, request.AuthCode,))
            after = await self.Balance(atm_pb2.BalanceRequest(AuthCode=request.AuthCode), context)
            if after == current:
                return atm_pb2.DepositReply(success=False, error="Invalid input")
            else:
                return atm_pb2.DepositReply(success=True)
        except Exception as e:
            return atm_pb2.DepositReply(success=False, error="Backend error")



async def serve() -> None:
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=16))
    atm_pb2_grpc.add_AtmServicer_to_server(AtmServicer(), server)
    listen_addr = '[::]:50051'
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()

    async def server_graceful_shutdown():
        logging.info("Starting shutdown...")
        await server.stop(0)

    _cleanup_coroutines.append(server_graceful_shutdown())
    await server.wait_for_termination()



if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(serve())
    finally:
        loop.run_until_complete(*_cleanup_coroutines)
        loop.close()
