import asyncio
import logging
from decimal import Decimal, getcontext
from typing import Tuple

import grpc

import atm_pb2
import atm_pb2_grpc

getcontext().prec = 13 + 4


class BadRequest(Exception):
    def __init__(self, message):
        self.message = message

        super().__init__(self.message)

    def __str__(self):
        return self.message


class AtmClient:
    def __init__(self, username, pin, host, port):
        self.username = str(username)
        self.pin = int(pin)
        self.AuthCode = None
        self.host = host
        self.port = port
        self.channel = None
        self.stub = None

    async def connect(self):
        self.channel = grpc.aio.insecure_channel(f"{self.host}:{self.port}")
        self.stub = atm_pb2_grpc.AtmStub(self.channel)

    async def authenticate(self):
        try:
            response = await self.stub.Authenticate(atm_pb2.AuthenticateRequest(username=self.username, pin=self.pin))
            if response.success:
                self.AuthCode = response.AuthCode
                return "Authenticated"
            else:
                return response.error
        except Exception as e:
            return "Error with request"

        self.AuthCode = str(response.AuthCode)

    async def getBalance(self) -> Decimal:
        try:
            response = await self.stub.Balance(atm_pb2.BalanceRequest(AuthCode=self.AuthCode))
            if response.success:
                return Decimal((Decimal(response.units) / Decimal(response.denomination)))
            else:
                return response.error
        except Exception as e:
            return "Error with request"

    async def withdraw(self, amount: Decimal):
        try:
            amount = Decimal(amount)
            amount: tuple[int, int] = amount.as_integer_ratio()
            response = await self.stub.Withdraw(
                atm_pb2.WithdrawRequest(AuthCode=self.AuthCode, units=(amount[0]), denomination=amount[1]))
            if not response.success:
                return response.error
        except Exception as e:
            print(e)

    async def deposit(self, amount: Decimal):
        try:
            amount = Decimal(amount)
            amount: tuple[int, int] = amount.as_integer_ratio()
            response = await self.stub.Deposit(
                atm_pb2.DepositRequest(AuthCode=self.AuthCode, units=(amount[0]), denomination=amount[1]))
            if not response.success:
                return response.error
        except Exception as e:
            print(e)

    async def close(self):
        await self.channel.close()
