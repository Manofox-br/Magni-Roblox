import sqlalchemy as sql
from sqlalchemy.orm import declarative_base, sessionmaker

engine = sql.create_engine("sqlite:///database/discord.db")
Base = declarative_base()
Session_base = sessionmaker(engine)

class UserVars(Base):
  __tablename__ = "UserVars"
  id = sql.Column(sql.Integer, primary_key=True)
  name = sql.Column(sql.String)
  value = sql.Column(sql.Unicode)
  userID = sql.Column(sql.Integer)
  guildID = sql.Column(sql.Integer, nullable=True)
  def __repr__(self):
    return f"<UserVars(name={self.name}, value={self.value}, userID={self.userID}, guildID={self.guildID})>"
  
class ChannelVars(Base):
  __tablename__ = "ChannelVars"
  id = sql.Column(sql.Integer, primary_key=True)
  name = sql.Column(sql.String)
  value = sql.Column(sql.Unicode)
  channelID = sql.Column(sql.Integer)
  userID = sql.Column(sql.Integer, nullable=True)
  def __repr__(self):
    return f"<ChannelVars(name={self.name}, value={self.value}, ChannelID={self.channelID}, userID={self.userID})>"

class GuildVars(Base):
  __tablename__ = "GuildVars"
  id = sql.Column(sql.Integer, primary_key=True)
  name = sql.Column(sql.String)
  value = sql.Column(sql.Unicode)
  guildID = sql.Column(sql.Integer, nullable=True)
  def __repr__(self):
    return f"<GuildsVars(name={self.name}, value={self.value}, guildID={self.guildID})>"

Base.metadata.create_all(engine)

def setUserVar(name:str, value:str, userID:int, guildID:int = None):
  with Session_base() as session:
    query = session.query(UserVars).filter_by(name=name, userID=userID)
    if guildID is not None:
      query = query.filter_by(guildID=guildID)
    existente = query.first()
    if existente:
      existente.value = value
    else:
      vars = UserVars(name=name, value=value, userID=userID, guildID=guildID)
      session.add(vars)
    session.commit()

def getUserVar(name:str, userID:int, guildID:int = None):
  with Session_base() as session:
    query = session.query(UserVars).filter_by(name=name, userID=userID)
    if guildID is not None:
      query = query.filter_by(guildID=guildID)
    result = query.first()
    return result.value if result else None

def deleteUserVar(name:str, userID:int, guildID:int = None):
  with Session_base() as session:
    query = session.query(UserVars).filter_by(name=name, userID=userID)
    if guildID is not None:
      query = query.filter_by(guildID=guildID)
    existing = query.first()
    if existing:
      session.delete(existing)
      session.commit()
      return True
    #raise VarDeleted(f"It was not possible to delete the variable.")
    return False

def setChannelVar(name:str, value:str, channelID:int, userID:int = None):
  with Session_base() as session:
    query = session.query(ChannelVars).filter_by(name=name, channelID=channelID)
    if userID is not None:
     query = query.filter_by(userID=userID)
    existing = query.first()
    if existing:
      existing.value = value
    else:
      vars = ChannelVars(name=name, value=value, channelID=channelID, userID=userID)
      session.add(vars)
    session.commit()

def getChannelVar(name:str, channelID:int, userID:int = None):
  with Session_base() as session:
    query = session.query(ChannelVars).filter_by(name=name, channelID=channelID)
    if userID is not None:
      query = query.filter_by(userID=userID)
    if guildID is not None:
      query = query.filter_by(guildID=guildID)
    result = query.first()
    return result.value if result else None

def deleteChannelVar(name:str, channelID:int, userID:int = None, guildID:int = None):
  with Session_base() as session:
    query = session.query(ChannelVars).filter_by(name=name, channelID=channelID)
    if userID is not None:
      query = query.filter_by(userID=userID)
    if guildID is not None:
        query = query.filter_by(guildID=guildID)
    existing = query.first()
    if existing:
      session.delete(existing)
      session.commit()
      return True
    return False

def setServerVar(name:str, value:str, guildID:int):
  with Session_base() as session:
    query = session.query(GuildVars).filter_by(name=name, guildID=guildID)
    existing = query.first()
    if existing:
      existing.value = value
    else:
      vars = GuildVars(name=name, value=value, guildID=guildID)
      session.add(vars)
    session.commit()

def getServerVar(name:str, guildID:int):
  with Session_base() as session:
    query = session.query(GuildVars).filter_by(name=name, guildID=guildID)
    result = query.first()
    return result.value if result else None

def deleteServerVar(name:str, guildID:int):
  with Session_base as session:
    query = session.query(GuildVars).filter_by(name=name, guildID=guildID)
    existing = query.first()
    if existing:
      session.delete(existing)
      session.commit()
      return True
    return False

#setServerVar("teste", "valor2", 123)
#dados = getServerVar("teste", 123)
#print(dados)