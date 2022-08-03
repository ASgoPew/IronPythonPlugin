def status(player, text):
	player.SendData(PacketTypes.Status, text)

def iterate_players(f, condition):
	for i in range(Main.maxPlayers):
		p = TShock.Players[i]
		if p is not None and p.Active and (condition is None or condition(p)):
			f(p)

def check_control_permission(player):
	return player.HasPermission(IronPythonConfig.ControlPermission)

def firework(player):
	proj = Projectile.NewProjectile(player.TPlayer.position.X, player.TPlayer.position.Y - 64, 0, 0, random.randint(167, 170), 0, 0)
	if proj >= 0 and Main.projectile[proj] is not None:
		everyone.SendData(PacketTypes.ProjectileDestroy, None, proj, 255)

class GemsparkTileOn:
   Purple = 262
   Yellow = 263
   Blue = 264
   Green = 265
   Red = 266
   White = 267
   Orange = 268

class GemsparkTileOff:
   Purple = 255
   Yellow = 256
   Blue = 257
   Green = 258
   Red = 259
   White = 260
   Orange = 261

class GemsparkWallOn:
	Orange = 153
	Purple = 154
	White = 155
	Green = 156
	Red = 164
	Blue = 165
	Yellow = 166

class GemsparkWallOff:
	Orange = 157
	Purple = 158
	White = 159
	Green = 160
	Red = 161
	Blue = 162
	Yellow = 163

class Slope:
	No = 0
	DownRight = 1
	DownLeft = 2
	UpRight = 3
	UpLeft = 4

def signs():
	return [(i, Main.sign[i].text, Main.sign[i].x, Main.sign[i].y, Main.sign[i].GetHashCode()) for i in range(1000) if Main.sign[i] is not None]
def chests():
	return [(i, Main.chest[i].name, Main.chest[i].x, Main.chest[i].y, Main.chest[i].GetHashCode()) for i in range(1000) if Main.chest[i] is not None]
def ents():
	return [(e.ID, e.GetType().Name, e.Position.X, e.Position.Y) for e in TileEntity.ByID.Values]
def ents2():
	return [(e.ID, e.GetType().Name, e.Position.X, e.Position.Y) for e in TileEntity.ByPosition.Values]
def npcs():
	return [(i, Main.npc[i].netID, Main.npc[i].position.X/16, Main.npc[i].position.Y/16) for i in range(200) if Main.npc[i].active]

def class_or_subclass(o, cls):
	return o.GetType() == cls or o.GetType().IsSubclassOf(cls)

def entity_str(e):
	if class_or_subclass(e, Sign):
		return "%s (%s, %s, %s)" % (e.GetType().Name, e.x, e.y, e.text)
	elif class_or_subclass(e, Chest):
		return "%s (%s, %s)" % (e.GetType().Name, e.x, e.y)
	elif class_or_subclass(e, TETrainingDummy) or class_or_subclass(e, TEItemFrame) or class_or_subclass(e, TELogicSensor):
		return "%s (%s, %s, %s)" % (e.GetType().Name, e.Position.X, e.Position.Y, e.ID)