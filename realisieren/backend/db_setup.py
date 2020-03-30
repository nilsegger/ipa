import asyncpg
import asyncio

LOGIN_TABLE = """
        CREATE TABLE IF NOT EXISTS logins(
            uuid UUID PRIMARY KEY NOT NULL,
            username varchar(30) NOT NULL,
            role varchar(15) NOT NULL,
            password bytea NOT NULL,
            salt bytea NOT NULL,
            mem_cost int2 NOT NULL,
            rounds int2 NOT NULL,
            refresh_token varchar(683),
            refresh_token_expires timestamp,
            refresh_token_revoked boolean
        )
"""

PERSONAL_TABLE = """
    CREATE TYPE Rolle AS ENUM ('ADMIN', 'PERSONAL');
    CREATE TABLE Personal(
        uuid UUID PRIMARY KEY,
        name varchar(100),
        FOREIGN KEY (uuid) REFERENCES logins(uuid)
    );
"""

GEBAEUDE_TABLE = """
    CREATE TABLE Gebaeude(
        id SERIAL4 PRIMARY KEY,
        name varchar(100) NOT NULL
    );
"""

STOCKWERKE_TABLE = """
    CREATE TABLE Stockwerke(
        id SERIAL4 PRIMARY KEY,
        idGebaeude int4 NOT NULL,
        name varchar(100) NOT NULL,
        niveau int NOT NULL,
        FOREIGN KEY (idGebaeude) REFERENCES Gebaeude(id)
    );
"""

RAEUME_TABLE = """
    CREATE TABLE Raeume(
        id SERIAL4 PRIMARY KEY,
        idStockwerk int4 NOT NULL,
        name varchar(100) NOT NULL,
        FOREIGN KEY (idStockwerk) REFERENCES Stockwerke(id)
    );
"""

SENSOREN_TABLE = """
    CREATE TYPE SensorArt as ENUM ('ADEUNIS_RF', 'ELSYS_ERS_CO2', 'TABS');
    CREATE TABLE Sensoren(
        dev_eui VARCHAR(16) PRIMARY KEY,
        idRaum int4 NOT NULL,
        art SensorArt NOT NULL,
        name VARCHAR(100) NOT NULL,
        FOREIGN KEY (idRaum) REFERENCES Raeume(id)
    );
"""

SENSOR_WERTE_TABLE = """
    CREATE TABLE SensorenWerte(
        id SERIAL4 PRIMARY KEY,
        dev_euiSensor VARCHAR(16) NOT NULL,
        rohWert VARCHAR NOT NULL,
        dekodiertJSON TEXT NOT NULL,
        erhalten timestamp NOT NULL,
        FOREIGN KEY (dev_euiSensor) REFERENCES Sensoren(dev_eui)
    );
"""

BEOBACHTER_TABLE = """
    CREATE TYPE BeobachterArt AS ENUM ('RICHTWERT_DARUEBER', 'RICHTWERT_DARUNTER', 'ZAEHLERSTAND'); 
    CREATE TABLE Beobachter(
        id SERIAL4 PRIMARY KEY,
        dev_euiSensor VARCHAR(16) NOT NULL,
        name VARCHAR(100) NOT NULL,
        art BeobachterArt NOT NULL,
        wertName VARCHAR(100) NOT NULL,
        ausloeserWert int NOT NULL,
        stand int DEFAULT 0
        FOREIGN KEY (dev_euiSensor) REFERENCES Sensoren(dev_eui)
    );
"""

MELDUNGEN_TABLE = """
    CREATE TYPE MeldungsArt AS ENUM('AUTO', 'MANUELL');
    CREATE TABLE Meldungen(
        id SERIAL4 PRIMARY KEY,
        dev_euiSensor VARCHAR(16),
        idBeobachter int,
        idRaum int4 NOT NULL,
        uuidPersonal UUID,
        art MeldungsArt NOT NULL,
        datum timestamp NOT NULL,
        bearbeitet boolean DEFAULT false,
        beschreibung TEXT NOT NULL,
        FOREIGN KEY (dev_euiSensor) REFERENCES Sensoren(dev_eui),
        FOREIGN KEY (idRaum) REFERENCES Raeume(id),
        FOREIGN KEY (uuidPersonal) REFERENCES Personal(uuid)
        FOREIGN KEY (idBeobachter) REFERENCES Beobachter(id)
    );
"""

MATERIAL_TABLE = """
    CREATE TABLE Materialien(
        id SERIAL4 PRIMARY KEY,
        name varchar(100)
    );
"""

MATERIAL_ZU_BEOBACHTER_TABLE = """
    CREATE TABLE MaterialZuBeobachter(
        id SERIAL4 PRIMARY KEY,
        idMaterial int4 NOT NULL,
        idBeobachter int4 NOT NULL,
        anzahl int DEFAULT 1,
        FOREIGN KEY (idMaterial) REFERENCES Materialien(id),
        FOREIGN KEY (idBeobachter) REFERENCES Beobachter(id)
    );
"""


async def create_tables():
    connection = await asyncpg.connect(host='localhost', database='bbb',
                                       user='postgres', password='postgres')
    await connection.execute(GEBAEUDE_TABLE)
    await connection.execute(STOCKWERKE_TABLE)
    await connection.execute(RAEUME_TABLE)
    await connection.execute(LOGIN_TABLE)
    await connection.execute(PERSONAL_TABLE)
    await connection.execute(SENSOREN_TABLE)
    await connection.execute(SENSOR_WERTE_TABLE)
    await connection.execute(MATERIAL_TABLE)
    await connection.execute(BEOBACHTER_TABLE)
    await connection.execute(MATERIAL_ZU_BEOBACHTER_TABLE)
    await connection.execute(MELDUNGEN_TABLE)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(create_tables())
