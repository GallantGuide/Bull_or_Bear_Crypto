CREATE TABLE "COINS" (
    "Symbol" varchar(6)   UNIQUE,
    "Name" varchar   NOT NULL,
);

CREATE TABLE "BITCOIN" (
    "Date" date   NOT NULL,
    "Open" decimal   NOT NULL,
    "High" decimal   NOT NULL,
    "low" decimal   NOT NULL,
    "close" decimal   NOT NULL,
    "adjClose" decimal   NOT NULL,
    "Volume" decimal   NOT NULL,
    "Symbol" varchar(6)   NOT NULL
);

CREATE TABLE "ETHEREUM" (
    "Date" date   NOT NULL,
    "Open" decimal   NOT NULL,
    "High" decimal   NOT NULL,
    "low" decimal   NOT NULL,
    "close" decimal   NOT NULL,
    "adjClose" decimal   NOT NULL,
    "Volume" decimal   NOT NULL,
    "Symbol" varchar(6)   NOT NULL
);

CREATE TABLE "LITECOIN" (
    "Date" date   NOT NULL,
    "Open" decimal   NOT NULL,
    "High" decimal   NOT NULL,
    "low" decimal   NOT NULL,
    "close" decimal   NOT NULL,
    "adjClose" decimal   NOT NULL,
    "Volume" decimal   NOT NULL,
    "Symbol" varchar(6)   NOT NULL
);

CREATE TABLE "CARDANO" (
    "Date" date   NOT NULL,
    "Open" decimal   NOT NULL,
    "High" decimal   NOT NULL,
    "low" decimal   NOT NULL,
    "close" decimal   NOT NULL,
    "adjClose" decimal   NOT NULL,
    "Volume" decimal   NOT NULL,
    "Symbol" varchar(6)   NOT NULL
);

CREATE TABLE "RIPPLE" (
    "Date" date   NOT NULL,
    "Open" decimal   NOT NULL,
    "High" decimal   NOT NULL,
    "low" decimal   NOT NULL,
    "close" decimal   NOT NULL,
    "adjClose" decimal   NOT NULL,
    "Volume" decimal   NOT NULL,
    "Symbol" varchar(6)   NOT NULL
);

CREATE TABLE "BINANCE" (
    "Date" date   NOT NULL,
    "Open" decimal   NOT NULL,
    "High" decimal   NOT NULL,
    "low" decimal   NOT NULL,
    "close" decimal   NOT NULL,
    "adjClose" decimal   NOT NULL,
    "Volume" decimal   NOT NULL,
    "Symbol" varchar(6)   NOT NULL
);

CREATE TABLE "CHAINLINK" (
    "Date" date   NOT NULL,
    "Open" decimal   NOT NULL,
    "High" decimal   NOT NULL,
    "low" decimal   NOT NULL,
    "close" decimal   NOT NULL,
    "adjClose" decimal   NOT NULL,
    "Volume" decimal   NOT NULL,
    "Symbol" varchar(6)   NOT NULL
);

CREATE TABLE "DOGECOIN" (
    "Date" date   NOT NULL,
    "Open" decimal   NOT NULL,
    "High" decimal   NOT NULL,
    "low" decimal   NOT NULL,
    "close" decimal   NOT NULL,
    "adjClose" decimal   NOT NULL,
    "Volume" decimal   NOT NULL,
    "Symbol" varchar(6)   NOT NULL
);

CREATE TABLE "ETHEREUM_CLASSIC" (
    "Date" date   NOT NULL,
    "Open" decimal   NOT NULL,
    "High" decimal   NOT NULL,
    "low" decimal   NOT NULL,
    "close" decimal   NOT NULL,
    "adjClose" decimal   NOT NULL,
    "Volume" decimal   NOT NULL,
    "Symbol" varchar(6)   NOT NULL
);

CREATE TABLE "POLKADOT" (
    "Date" date   NOT NULL,
    "Open" decimal   NOT NULL,
    "High" decimal   NOT NULL,
    "low" decimal   NOT NULL,
    "close" decimal   NOT NULL,
    "adjClose" decimal   NOT NULL,
    "Volume" decimal   NOT NULL,
    "Symbol" varchar(6)   NOT NULL
);

CREATE TABLE "SOLANA" (
    "Date" date   NOT NULL,
    "Open" decimal   NOT NULL,
    "High" decimal   NOT NULL,
    "low" decimal   NOT NULL,
    "close" decimal   NOT NULL,
    "adjClose" decimal   NOT NULL,
    "Volume" decimal   NOT NULL,
    "Symbol" varchar(6)   NOT NULL
);

CREATE TABLE "COSMOS" (
    "Date" date   NOT NULL,
    "Open" decimal   NOT NULL,
    "High" decimal   NOT NULL,
    "low" decimal   NOT NULL,
    "close" decimal   NOT NULL,
    "adjClose" decimal   NOT NULL,
    "Volume" decimal   NOT NULL,
    "Symbol" varchar(6)   NOT NULL
);

ALTER TABLE "BITCOIN" ADD CONSTRAINT "fk_BITCOIN_Symbol" FOREIGN KEY("Symbol")
REFERENCES "COINS" ("Symbol");

ALTER TABLE "ETHEREUM" ADD CONSTRAINT "fk_ETHEREUM_Symbol" FOREIGN KEY("Symbol")
REFERENCES "COINS" ("Symbol");

ALTER TABLE "LITECOIN" ADD CONSTRAINT "fk_LITECOIN_Symbol" FOREIGN KEY("Symbol")
REFERENCES "COINS" ("Symbol");

ALTER TABLE "CARDANO" ADD CONSTRAINT "fk_CARDANO_Symbol" FOREIGN KEY("Symbol")
REFERENCES "COINS" ("Symbol");

ALTER TABLE "RIPPLE" ADD CONSTRAINT "fk_RIPPLE_Symbol" FOREIGN KEY("Symbol")
REFERENCES "COINS" ("Symbol");

ALTER TABLE "BINANCE" ADD CONSTRAINT "fk_BINANCE_Symbol" FOREIGN KEY("Symbol")
REFERENCES "COINS" ("Symbol");

ALTER TABLE "CHAINLINK" ADD CONSTRAINT "fk_CHAINLINK_Symbol" FOREIGN KEY("Symbol")
REFERENCES "COINS" ("Symbol");

ALTER TABLE "DOGECOIN" ADD CONSTRAINT "fk_DOGECOIN_Symbol" FOREIGN KEY("Symbol")
REFERENCES "COINS" ("Symbol");

ALTER TABLE "ETHEREUM_CLASSIC" ADD CONSTRAINT "fk_ETHEREUM_CLASSIC_Symbol" FOREIGN KEY("Symbol")
REFERENCES "COINS" ("Symbol");

ALTER TABLE "POLKADOT" ADD CONSTRAINT "fk_POLKADOT_Symbol" FOREIGN KEY("Symbol")
REFERENCES "COINS" ("Symbol");

ALTER TABLE "SOLANA" ADD CONSTRAINT "fk_SOLANA_Symbol" FOREIGN KEY("Symbol")
REFERENCES "COINS" ("Symbol");

ALTER TABLE "COSMOS" ADD CONSTRAINT "fk_COSMOS_Symbol" FOREIGN KEY("Symbol")
REFERENCES "COINS" ("Symbol");