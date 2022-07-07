#!/usr/bin/env python3
from modules.common import simcount
from modules.common.component_state import BatState
from modules.common.fault_state import ComponentInfo
from modules.common.modbus import ModbusClient, ModbusDataType
from modules.common.store import get_bat_value_store


def get_default_config() -> dict:
    return {
        "name": "SMA Sunny Boy Smart Energy Speicher",
        "id": 0,
        "type": "bat_smart_energy",
        "configuration": {}
    }


class SunnyBoySmartEnergyBat:
    def __init__(self, device_id: int, component_config: dict, tcp_client: ModbusClient) -> None:
        self.__device_id = device_id
        self.component_config = component_config
        self.__tcp_client = tcp_client
        self.__sim_count = simcount.SimCountFactory().get_sim_counter()()
        self.simulation = {}
        self.__store = get_bat_value_store(component_config["id"])
        self.component_info = ComponentInfo.from_component_config(component_config)

    def update(self) -> None:
        unit = 3
        with self.__tcp_client:
            soc = self.__tcp_client.read_holding_registers(30845, ModbusDataType.UINT_32, unit=unit)
            current = self.__tcp_client.read_holding_registers(30843, ModbusDataType.INT_32, unit=unit)/-1000
            voltage = self.__tcp_client.read_holding_registers(30851, ModbusDataType.INT_32, unit=unit)/100

        power = current*voltage
        topic_str = "openWB/set/system/device/" + str(
            self.__device_id)+"/component/"+str(self.component_config["id"])+"/"
        imported, exported = self.__sim_count.sim_count(
            power, topic=topic_str, data=self.simulation, prefix="speicher"
        )

        bat_state = BatState(
            power=power,
            soc=soc,
            imported=imported,
            exported=exported
        )
        self.__store.set(bat_state)
