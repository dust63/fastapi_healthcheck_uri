from fastapi_healthcheck.domain import HealthCheckInterface
from fastapi_healthcheck.service import HealthCheckBase
from fastapi_healthcheck.enum import HealthCheckStatusEnum
from typing import Dict, List
from requests import get


class HealthCheckUri(HealthCheckBase, HealthCheckInterface):
    _tags: List[str]
    _connectionUri: str
    _healthyCode: int
    _unhealthyCode: int
    _ssl_verify: bool
    _headers: Dict
    _timeout: float | None

    def __init__(
        self,
        connectionUri: str,
        alias: str,
        tags: List[str],
        healthyCode: int = 200,
        unhealthyCode: int = 500,
        ssl_verify: bool = True,
        headers: Dict = {},
        timeout: float | None = None,
    ) -> None:
        self.setConnectionUri(connectionUri)
        self._alias = alias
        self._tags = tags
        self._healthyCode = healthyCode
        self._unhealthyCode = unhealthyCode
        self._ssl_verify = ssl_verify
        self._headers = headers
        self._timeout = timeout

    def __checkHealth__(self) -> bool:
        try:
            res = get(
                url=self.getConnectionUri(),
                headers={"User-Agent": "FastAPI HealthCheck"} | self._headers,
                timeout=self._timeout,
                verify=self._ssl_verify,
            )
            if res.status_code == self._healthyCode:
                return HealthCheckStatusEnum.HEALTHY
            if res.status_code != self._unhealthyCode:
                return HealthCheckStatusEnum.UNHEALTHY
        except:  # pylint: disable=W0702
            return HealthCheckStatusEnum.UNHEALTHY

        return HealthCheckStatusEnum.UNHEALTHY
