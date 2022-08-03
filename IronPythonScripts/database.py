def connect_db(db_name=None):
	if TShock.Config.StorageType.ToLower() == "sqlite":
		db = SqliteConnection("uri=file://%s,Version=3"
			% (db_name if db_name is not None else Path.Combine(TShock.SavePath, "tshock.sqlite")))
	elif TShock.Config.StorageType.ToLower() == "mysql":
		host = TShock.Config.MySqlHost.Split(':')
		db = MySqlConnection(ConnectionString =
			"Server=%s; Port=%s; Database=%s; Uid=%s; Pwd=%s"
			% (host[0],
				"3306" if host.Length == 1 else host[1],
				TShock.Config.MySqlDbName if db_name is None else db_name,
				TShock.Config.MySqlUsername,
				TShock.Config.MySqlPassword))
	else:
		raise Exception("Invalid database storage type.")
	return db

def db_query(db, query):
	success = False
	db.Open()
	try:
		with db.CreateCommand() as conn:
			conn.CommandText = query
			conn.ExecuteNonQuery()
			success = True
	finally:
		db.Close()
	return success

def db_read(db, query, readf):
	count = 0
	db.Open()
	try:
		with db.CreateCommand() as cmd:
			cmd.CommandText = query
			with cmd.ExecuteReader() as reader:
				while reader.Read():
					count += 1
					readf(reader)
	finally:
		db.Close()
	return count