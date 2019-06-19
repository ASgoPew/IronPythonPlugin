clr.AddReferenceByName("IronPythonPlugin")
from IronPythonPlugin import *

clr.AddReferenceByName("OTAPI")
from Terraria import *
from Terraria.ID import *

clr.AddReferenceByName("TShockAPI")
from TShockAPI.Hooks import *
import TShockAPI
from TShockAPI import TSPlayer, GetDataHandlers, TShock, PlayerData, NetItem, Commands

clr.AddReferenceByName("TerrariaServer")
from TerrariaApi.Server import *
import PacketTypes