clr.AddReferenceByName("IronPythonPlugin")
from IronPythonPlugin import *

clr.AddReferenceByName("OTAPI")
from Terraria import *
from Terraria.ID import *
from Terraria.DataStructures import *
from Terraria.GameContent.Tile_Entities import *
from OTAPI.Tile import ITile

clr.AddReferenceByName("TShockAPI")
from TShockAPI.Hooks import *
import TShockAPI
from TShockAPI import TSPlayer, GetDataHandlers, TShock, PlayerData, NetItem, Commands

clr.AddReferenceByName("TerrariaServer")
from TerrariaApi.Server import *
import PacketTypes

clr.AddReferenceByName("Newtonsoft.Json")
from Newtonsoft.Json import *

try:
	clr.AddReferenceByName("BestProxyPlugin")
	from BestProxyPlugin import BestProxyPlugin
except:
	BestProxyPlugin = None

try:
	clr.AddReferenceByName("TUI")
	from TerrariaUI import *
	from TerrariaUI.Base import *
	from TerrariaUI.Base.Style import *
	from TerrariaUI.Widgets import *
	from TerrariaUI.Widgets.Media import *
	from TerrariaUI.Widgets.Data import *

	clr.AddReferenceByName("TUIPlugin")
	from TUIPlugin import *
	import TUIPlugin
	clr.ImportExtensions(TUIPlugin)
except:
	TUI = None

try:
	clr.AddReferenceByName("PvPModifier")
	from PvPModifier.DataStorage import Cache
	PvPModifier = True
except:
	PvPModifier = None

try:
	clr.AddReferenceByName("GhostPlayers")
	from GhostPlayers import *
except:
	GPAPI = None

try:
	clr.AddReferenceByName("FakePlayers")
	from FakePlayers import *
except:
	FPAPI = None

try:
	clr.AddReferenceByName("FakeProvider")
	from FakeProvider import FakeProviderAPI, FakeSign, FakeChest, FakeTrainingDummy, FakeItemFrame, FakeLogicSensor
except:
	FakeProviderAPI = None
FakeManager = None

try:
	clr.AddReferenceByName("SSCManager")
	import SSCManager
	clr.ImportExtensions(SSCManager)
except:
	SSCManager = None

clr.AddReferenceByName("Mono.Data.Sqlite")
from Mono.Data.Sqlite import SqliteConnection

clr.AddReferenceByName("MySql.Data")
from MySql.Data.MySqlClient import MySqlConnection


try:
	clr.AddReferenceByName("PedguinServer")
	import PedguinServer
	clr.ImportExtensions(PedguinServer)
	from PedguinServer import PluginLogic
except:
	PedguinServer = None