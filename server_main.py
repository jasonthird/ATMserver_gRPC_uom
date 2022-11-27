import asyncio
import logging
from concurrent import futures
from decimal import Decimal, getcontext

import grpc
import mariadb

import SqlConnection
import atm_pb2
import atm_pb2_grpc
from atm_pb2_grpc import AtmServicer

_cleanup_coroutines = []
getcontext().prec = 23


class AtmServicer(AtmServicer):

    async def Authenticate(self, request, context):
        sql = SqlConnection.Sql()
        try:
            Auth = sql.AuthUser(request.username, request.pin)
            if Auth is False:
                return atm_pb2.AuthenticateResponse(success=False, error="Wrong pin or username")
            else:
                return atm_pb2.AuthenticateResponse(success=True, AuthCode=Auth)
        except mariadb.Error as e:
            print(e)
            return atm_pb2.AuthenticateResponse(success=False, error="Backend error")

    async def Balance(self, request, context):
        sql = SqlConnection.Sql()
        try:
            response = sql.getBalance(request.AuthCode)
            if response is False:
                return atm_pb2.BalanceReply(success=False, error="Invalid AuthCode")
            else:
                d = Decimal(response).as_integer_ratio()
                return atm_pb2.BalanceReply(success=True, units=d[0], denomination=d[1])
        except mariadb.Error as e:
            print(e)
            return atm_pb2.BalanceReply(success=False, error="Backend error")

    async def Withdraw(self, request, context):
        sql = SqlConnection.Sql()
        money = Decimal(Decimal(request.units) / Decimal(request.denomination))
        try:
            sqlAwnser = sql.Withdraw(request.AuthCode, money)
            if sqlAwnser[0] == sqlAwnser[1]:
                return atm_pb2.WithdrawReply(success=False, error="Invalid input")
            else:
                return atm_pb2.WithdrawReply(success=True)
        except mariadb.Error as e:
            print(e)
            return atm_pb2.WithdrawReply(success=False, error="Backend error")

    async def Deposit(self, request, context):
        sql = SqlConnection.Sql()
        money = Decimal(Decimal(request.units) / Decimal(request.denomination))
        try:
            sqlAwnser = sql.Deposit(request.AuthCode, money)
            if sqlAwnser[0] == sqlAwnser[1]:
                return atm_pb2.DepositReply(success=False, error="Invalid input")
            else:
                return atm_pb2.DepositReply(success=True)
        except mariadb.Error as e:
            print(e)
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
