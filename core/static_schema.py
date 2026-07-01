"""
Static schema registry — paste all 30 table DDLs here.
No DB round-trip needed; loaded once at import time.

FORMAT per table:
  SCHEMA[table_name] = [
      {"column": "...", "type": "...", "nullable": "YES/NO", "max_length": N or None},
      ...
  ]

METADATA per column (for semantic search / glossary injection):
  COLUMN_META[table_name.column_name] = {
      "alias":       "plain English name",
      "description": "what this column means",
      "tags":        ["tag1", "tag2"],
  }
"""

from __future__ import annotations

# ══════════════════════════════════════════════════════════════════════════════
#  SCHEMA — raw column definitions (mirrors CREATE TABLE statements)
# ══════════════════════════════════════════════════════════════════════════════

SCHEMA: dict[str, list[dict]] = {

    "fingate_CbwtrBank": [
        {"column": "transactionId",                 "type": "nvarchar",   "nullable": "YES", "max_length": 50},
        {"column": "transactionDate",               "type": "datetime2",  "nullable": "YES", "max_length": None},
        {"column": "trasactionTime",                "type": "nvarchar",   "nullable": "YES", "max_length": 30},
        {"column": "txCurrencyCode",                "type": "bigint",     "nullable": "YES", "max_length": None},
        {"column": "amountInInr",                   "type": "decimal",    "nullable": "YES", "max_length": None},
        {"column": "amountInTxCurrency",            "type": "decimal",    "nullable": "YES", "max_length": None},
        {"column": "originCountry",                 "type": "bigint",     "nullable": "YES", "max_length": None},
        {"column": "institution",                   "type": "nvarchar",   "nullable": "YES", "max_length": 100},
        {"column": "destinationCountry",            "type": "bigint",     "nullable": "YES", "max_length": None},
        {"column": "senderName",                    "type": "nvarchar",   "nullable": "YES", "max_length": 100},
        {"column": "indentifierType",               "type": "nvarchar",   "nullable": "YES", "max_length": 30},
        {"column": "senderIdentifierAcNo",          "type": "nvarchar",   "nullable": "YES", "max_length": 75},
        {"column": "senderBankOrBic",               "type": "nvarchar",   "nullable": "YES", "max_length": 100},
        {"column": "senderAddressLine1",            "type": "nvarchar",   "nullable": "YES", "max_length": 255},
        {"column": "senderCountry",                 "type": "bigint",     "nullable": "YES", "max_length": None},
        {"column": "senderPinCode",                 "type": "nvarchar",   "nullable": "YES", "max_length": 10},
        {"column": "senderLocality",                "type": "nvarchar",   "nullable": "YES", "max_length": 255},
        {"column": "senderState",                   "type": "bigint",     "nullable": "YES", "max_length": None},
        {"column": "senderDistrict",                "type": "bigint",     "nullable": "YES", "max_length": None},
        {"column": "senderCityVillageTown",         "type": "bigint",     "nullable": "YES", "max_length": None},
        {"column": "benificiaryName",               "type": "nvarchar",   "nullable": "YES", "max_length": 100},
        {"column": "benificiaryBankOrBic",          "type": "nvarchar",   "nullable": "YES", "max_length": 100},
        {"column": "beneficiaryBankOrBic",          "type": "nvarchar",   "nullable": "YES", "max_length": 100},
        {"column": "beneficiaryAcNo",               "type": "nvarchar",   "nullable": "YES", "max_length": 50},
        {"column": "beneficiaryIdentifierType",     "type": "nvarchar",   "nullable": "YES", "max_length": 20},
        {"column": "beneficiaryIdentifierAcNo",     "type": "nvarchar",   "nullable": "YES", "max_length": 75},
        {"column": "benAddressLine1",               "type": "nvarchar",   "nullable": "YES", "max_length": 300},
        {"column": "benCountry",                    "type": "bigint",     "nullable": "YES", "max_length": None},
        {"column": "benPinCode",                    "type": "nvarchar",   "nullable": "YES", "max_length": 50},
        {"column": "benLocality",                   "type": "nvarchar",   "nullable": "YES", "max_length": 255},
        {"column": "benState",                      "type": "bigint",     "nullable": "YES", "max_length": None},
        {"column": "benDistrict",                   "type": "bigint",     "nullable": "YES", "max_length": None},
        {"column": "benCityVillageTown",            "type": "bigint",     "nullable": "YES", "max_length": None},
        {"column": "rbiCode",                       "type": "bigint",     "nullable": "YES", "max_length": None},
        {"column": "swiftMessageText",              "type": "nvarchar",   "nullable": "YES", "max_length": None},
        {"column": "swiftMessageCode",              "type": "nvarchar",   "nullable": "YES", "max_length": 30},
        {"column": "senderCorresBankOrBic",         "type": "nvarchar",   "nullable": "YES", "max_length": 100},
        {"column": "beneficiaryCorresBankOrBic",    "type": "nvarchar",   "nullable": "YES", "max_length": 100},
        {"column": "thirdReimInstBankOrBic",        "type": "nvarchar",   "nullable": "YES", "max_length": 100},
        {"column": "intermediaryInstBankOrBic",     "type": "nvarchar",   "nullable": "YES", "max_length": 100},
        {"column": "reportId",                      "type": "bigint",     "nullable": "YES", "max_length": None},
        {"column": "batchId",                       "type": "bigint",     "nullable": "YES", "max_length": None},
    ],

    # ── fingate_Gos ───────────────────────────────────────────────────────────
    "fingate_Gos": [
        {"column": "reportId",               "type": "bigint",    "nullable": "YES", "max_length": None},
        {"column": "batchId",                "type": "bigint",    "nullable": "YES", "max_length": None},
        {"column": "kycFundSource",          "type": "nvarchar",  "nullable": "YES", "max_length": 1000},
        {"column": "kycFundDestination",     "type": "nvarchar",  "nullable": "YES", "max_length": 1000},
        {"column": "gosTag1",                "type": "bigint",    "nullable": "YES", "max_length": None},
        {"column": "gosTag2",                "type": "nvarchar",  "nullable": "YES", "max_length": 75},
        {"column": "gosTag3",                "type": "nvarchar",  "nullable": "YES", "max_length": 30},
        {"column": "gosTextNarration",       "type": "nvarchar",  "nullable": "YES", "max_length": None},
        {"column": "gosTag4",                "type": "nvarchar",  "nullable": "YES", "max_length": 100},
        {"column": "otherOffenceType",       "type": "nvarchar",  "nullable": "YES", "max_length": 50},
        {"column": "status",                 "type": "int",       "nullable": "YES", "max_length": None},
        {"column": "statusByUserId",         "type": "bigint",    "nullable": "YES", "max_length": None},
        {"column": "statusByUserName",       "type": "nvarchar",  "nullable": "YES", "max_length": 75},
        {"column": "statusDate",             "type": "datetime2", "nullable": "YES", "max_length": None},
        {"column": "statusComment",          "type": "nvarchar",  "nullable": "YES", "max_length": 1024},
        {"column": "legacy_batch_id",        "type": "bigint",    "nullable": "YES", "max_length": None},
        {"column": "legacy_report_id",       "type": "bigint",    "nullable": "YES", "max_length": None},
        {"column": "migrated_flag",          "type": "char",      "nullable": "YES", "max_length": 1},
        {"column": "legacy_re_id",           "type": "nvarchar",  "nullable": "YES", "max_length": 20},
        {"column": "job_id",                 "type": "nvarchar",  "nullable": "YES", "max_length": 20},
        {"column": "otherRedFlagInd",        "type": "nvarchar",  "nullable": "YES", "max_length": 500},
        {"column": "attemptedTransaction",   "type": "nvarchar",  "nullable": "YES", "max_length": 5},
        {"column": "trasactionNotAvailable", "type": "nvarchar",  "nullable": "YES", "max_length": 5},
    ],

    # ── finnet_Currency ───────────────────────────────────────────────────────
    "finnet_Currency": [
        {"column": "id_",          "type": "bigint",   "nullable": "NO",  "max_length": None},
        {"column": "countryName",  "type": "nvarchar", "nullable": "YES", "max_length": 100},
        {"column": "currencyCode", "type": "nvarchar", "nullable": "YES", "max_length": 10},
        {"column": "description",  "type": "nvarchar", "nullable": "YES", "max_length": 100},
        {"column": "name",         "type": "nvarchar", "nullable": "YES", "max_length": 100},
        {"column": "countryCode",  "type": "nvarchar", "nullable": "YES", "max_length": 5},
    ],

    # ── finnet_Country ────────────────────────────────────────────────────────
    "finnet_Country": [
        {"column": "id_",         "type": "bigint",    "nullable": "NO",  "max_length": None},
        {"column": "name",        "type": "nvarchar",  "nullable": "YES", "max_length": 100},
        {"column": "countryCode", "type": "nvarchar",  "nullable": "YES", "max_length": 100},
        {"column": "isoCode",     "type": "nvarchar",  "nullable": "YES", "max_length": 100},
        {"column": "callCode",    "type": "nvarchar",  "nullable": "YES", "max_length": 100},
        {"column": "endDate",     "type": "datetime2", "nullable": "YES", "max_length": None},
    ],


    # ── fingate_KycSummary ────────────────────────────────────────────────────
    "fingate_KycSummary": [
        {"column": "primaryEntity",       "type": "nvarchar",   "nullable": "YES", "max_length": 3},
        {"column": "customer",            "type": "nvarchar",   "nullable": "YES", "max_length": 150},
        {"column": "entityType",          "type": "nvarchar",   "nullable": "YES", "max_length": 20},
        {"column": "entityName",          "type": "nvarchar",   "nullable": "YES", "max_length": 604},
        {"column": "UCICID",              "type": "nvarchar",   "nullable": "YES", "max_length": 50},
        {"column": "PAN",                 "type": "nvarchar",   "nullable": "YES", "max_length": 10},
        {"column": "uniqueID",            "type": "nvarchar",   "nullable": "YES", "max_length": 500},
        {"column": "risk",                "type": "nvarchar",   "nullable": "YES", "max_length": 10},
        {"column": "profession",          "type": "nvarchar",   "nullable": "YES", "max_length": 500},
        {"column": "incomePerYear",       "type": "decimal",    "nullable": "YES", "max_length": None},
        {"column": "reportId",            "type": "bigint",     "nullable": "YES", "max_length": None},
        {"column": "status",              "type": "int",        "nullable": "YES", "max_length": None},
        {"column": "statusByUserId",      "type": "bigint",     "nullable": "YES", "max_length": None},
        {"column": "statusByUserName",    "type": "nvarchar",   "nullable": "YES", "max_length": 75},
        {"column": "statusDate",          "type": "datetime2",  "nullable": "YES", "max_length": None},
        {"column": "statusComment",       "type": "nvarchar",   "nullable": "YES", "max_length": 1024},
        {"column": "legacy_batch_id",     "type": "bigint",     "nullable": "YES", "max_length": None},
        {"column": "legacy_report_id",    "type": "bigint",     "nullable": "YES", "max_length": None},
        {"column": "migrated_flag",       "type": "char",       "nullable": "YES", "max_length": 1},
        {"column": "legacy_re_id",        "type": "varchar",    "nullable": "YES", "max_length": 20},
        {"column": "rcd_create_date",     "type": "datetime2",  "nullable": "YES", "max_length": None},
        {"column": "BATCHID",             "type": "bigint",     "nullable": "YES", "max_length": None},
        {"column": "REPORTDATASETID",     "type": "bigint",     "nullable": "YES", "max_length": None},
        {"column": "REPORTREFERENCENO",   "type": "varchar",    "nullable": "YES", "max_length": 75},
    ],

    # ── fingate_AccountPerson ─────────────────────────────────────────────────
    "fingate_AccountPerson": [
        {"column": "accountNo",           "type": "nvarchar",   "nullable": "YES", "max_length": 50},
        {"column": "relationTypeId",      "type": "bigint",     "nullable": "YES", "max_length": None},
        {"column": "personType",          "type": "nvarchar",   "nullable": "YES", "max_length": 60},
        {"column": "ucic",                "type": "nvarchar",   "nullable": "YES", "max_length": 30},
        {"column": "reportId",            "type": "bigint",     "nullable": "YES", "max_length": None},
        {"column": "nonCustomerName",     "type": "nvarchar",   "nullable": "YES", "max_length": 100},
        {"column": "batchId",             "type": "bigint",     "nullable": "YES", "max_length": None},
        {"column": "reportDataSetId",     "type": "bigint",     "nullable": "YES", "max_length": None},
        {"column": "legacy_batch_id",     "type": "bigint",     "nullable": "YES", "max_length": None},
        {"column": "legacy_report_id",    "type": "bigint",     "nullable": "YES", "max_length": None},
        {"column": "migrated_flag",       "type": "char",       "nullable": "YES", "max_length": 1},
        {"column": "legacy_re_id",        "type": "nvarchar",   "nullable": "YES", "max_length": 20},
        {"column": "reportRefNo",         "type": "nvarchar",   "nullable": "YES", "max_length": 100},
        {"column": "reportType",          "type": "nvarchar",   "nullable": "YES", "max_length": 50},
    ],

    # ── fingate_AccountDetail ─────────────────────────────────────────────────
    "fingate_AccountDetail": [
        {"column": "batchId",                  "type": "bigint",    "nullable": "YES", "max_length": None},
        {"column": "reportId",                 "type": "bigint",    "nullable": "YES", "max_length": None},
        {"column": "accountType",              "type": "bigint",    "nullable": "YES", "max_length": None},
        {"column": "accountNumber",            "type": "nvarchar",  "nullable": "YES", "max_length": 50},
        {"column": "branchCode",               "type": "nvarchar",  "nullable": "YES", "max_length": 30},
        {"column": "acOpeningDate",            "type": "datetime2", "nullable": "YES", "max_length": None},
        {"column": "acClosingDate",            "type": "datetime2", "nullable": "YES", "max_length": None},
        {"column": "accountStatus",            "type": "nvarchar",  "nullable": "YES", "max_length": 15},
        {"column": "status",                   "type": "int",       "nullable": "YES", "max_length": None},
        {"column": "statusByUserId",           "type": "bigint",    "nullable": "YES", "max_length": None},
        {"column": "statusByUserName",         "type": "nvarchar",  "nullable": "YES", "max_length": 75},
        {"column": "statusDate",               "type": "datetime2", "nullable": "YES", "max_length": None},
        {"column": "statusComment",            "type": "nvarchar",  "nullable": "YES", "max_length": 1024},
        {"column": "legacy_batch_id",          "type": "bigint",    "nullable": "YES", "max_length": None},
        {"column": "legacy_report_id",         "type": "bigint",    "nullable": "YES", "max_length": None},
        {"column": "migrated_flag",            "type": "char",      "nullable": "YES", "max_length": 1},
        {"column": "legacy_re_id",             "type": "nvarchar",  "nullable": "YES", "max_length": 20},
        {"column": "job_id",                   "type": "nvarchar",  "nullable": "YES", "max_length": 20},
        {"column": "rcd_create_date",          "type": "datetime2", "nullable": "YES", "max_length": None},
        {"column": "rcd_upd d_update_date",    "type": "datetime2", "nullable": "YES", "max_length": None},
        {"column": "noofCashTxn",              "type": "varchar",   "nullable": "YES", "max_length": 100},
        {"column": "noofCredits",              "type": "varchar",   "nullable": "YES", "max_length": 100},
        {"column": "noofDebits",               "type": "varchar",   "nullable": "YES", "max_length": 100},
        {"column": "reasonActFreeze",          "type": "varchar",   "nullable": "YES", "max_length": 200},
        {"column": "totalCashDeposit",         "type": "varchar",   "nullable": "YES", "max_length": 100},
        {"column": "totalCashTxAmt",           "type": "varchar",   "nullable": "YES", "max_length": 100},
        {"column": "totalCreditAmount",        "type": "varchar",   "nullable": "YES", "max_length": 100},
        {"column": "totalDebitAmt",            "type": "varchar",   "nullable": "YES", "max_length": 100},
        {"column": "reportRefNo",              "type": "nvarchar",  "nullable": "YES", "max_length": 100},
        {"column": "reportType",               "type": "nvarchar",  "nullable": "YES", "max_length": 50},
    ],

    # ── fingate_EntityDetail ──────────────────────────────────────────────────
    "fingate_EntityDetail": [
        {"column": "ucic",                          "type": "nvarchar",  "nullable": "YES", "max_length": 30},
        {"column": "name",                          "type": "nvarchar",  "nullable": "YES", "max_length": 100},
        {"column": "uniqueCompanyId",               "type": "nvarchar",  "nullable": "YES", "max_length": 21},
        {"column": "pan",                           "type": "nvarchar",  "nullable": "YES", "max_length": 10},
        {"column": "panAvailability",               "type": "nvarchar",  "nullable": "YES", "max_length": 3},
        {"column": "tan",                           "type": "nvarchar",  "nullable": "YES", "max_length": 10},
        {"column": "gstin",                         "type": "nvarchar",  "nullable": "YES", "max_length": 15},
        {"column": "iec",                           "type": "nvarchar",  "nullable": "YES", "max_length": 20},
        {"column": "iecAvailability",               "type": "nvarchar",  "nullable": "YES", "max_length": 3},
        {"column": "pekrn",                         "type": "nvarchar",  "nullable": "YES", "max_length": 10},
        {"column": "telephoneNumber",               "type": "nvarchar",  "nullable": "YES", "max_length": 30},
        {"column": "mobileNumber",                  "type": "nvarchar",  "nullable": "YES", "max_length": 30},
        {"column": "emailId",                       "type": "nvarchar",  "nullable": "YES", "max_length": 100},
        {"column": "companyWebsite",                "type": "nvarchar",  "nullable": "YES", "max_length": 100},
        {"column": "addressLine1",                  "type": "nvarchar",  "nullable": "YES", "max_length": 255},
        {"column": "locality",                      "type": "nvarchar",  "nullable": "YES", "max_length": 255},
        {"column": "country",                       "type": "bigint",    "nullable": "YES", "max_length": None},
        {"column": "pinCode",                       "type": "nvarchar",  "nullable": "YES", "max_length": 12},
        {"column": "state",                         "type": "bigint",    "nullable": "YES", "max_length": None},
        {"column": "district",                      "type": "bigint",    "nullable": "YES", "max_length": None},
        {"column": "cityVillageTown",               "type": "bigint",    "nullable": "YES", "max_length": None},
        {"column": "linesOfBusiness",               "type": "nvarchar",  "nullable": "YES", "max_length": 200},
        {"column": "fcraStatus",                    "type": "nvarchar",  "nullable": "YES", "max_length": 3},
        {"column": "fcraRegState",                  "type": "bigint",    "nullable": "YES", "max_length": None},
        {"column": "fcraRegNumber",                 "type": "nvarchar",  "nullable": "YES", "max_length": 15},
        {"column": "regAddress",                    "type": "nvarchar",  "nullable": "YES", "max_length": 255},
        {"column": "regLocality",                   "type": "nvarchar",  "nullable": "YES", "max_length": 255},
        {"column": "regCountry",                    "type": "bigint",    "nullable": "YES", "max_length": None},
        {"column": "regPinCode",                    "type": "nvarchar",  "nullable": "YES", "max_length": 100},
        {"column": "regState",                      "type": "bigint",    "nullable": "YES", "max_length": None},
        {"column": "regDistrict",                   "type": "bigint",    "nullable": "YES", "max_length": None},
        {"column": "regCityVillageTown",            "type": "bigint",    "nullable": "YES", "max_length": None},
        {"column": "dateOfInc",                     "type": "datetime2", "nullable": "YES", "max_length": None},
        {"column": "customerType",                  "type": "bigint",    "nullable": "YES", "max_length": None},
        {"column": "lastkycDate",                   "type": "datetime2", "nullable": "YES", "max_length": None},
        {"column": "onboardingDate",                "type": "datetime2", "nullable": "YES", "max_length": None},
        {"column": "customerRiskLevel",             "type": "nvarchar",  "nullable": "YES", "max_length": 7},
        {"column": "ubo",                           "type": "varchar",   "nullable": "YES", "max_length": 100},
        {"column": "uboAvailability",               "type": "nvarchar",  "nullable": "YES", "max_length": 30},
        {"column": "reportId",                      "type": "bigint",    "nullable": "YES", "max_length": None},
        {"column": "batchId",                       "type": "bigint",    "nullable": "YES", "max_length": None},
        {"column": "reportDataSetId",               "type": "bigint",    "nullable": "YES", "max_length": None},
        {"column": "status",                        "type": "int",       "nullable": "YES", "max_length": None},
        {"column": "statusByUserId",                "type": "bigint",    "nullable": "YES", "max_length": None},
        {"column": "statusByUserName",              "type": "nvarchar",  "nullable": "YES", "max_length": 75},
        {"column": "statusDate",                    "type": "datetime2", "nullable": "YES", "max_length": None},
        {"column": "statusComment",                 "type": "nvarchar",  "nullable": "YES", "max_length": 1024},
        {"column": "stateName",                     "type": "nvarchar",  "nullable": "YES", "max_length": 100},
        {"column": "districtName",                  "type": "nvarchar",  "nullable": "YES", "max_length": 100},
        {"column": "cityVillageTownName",           "type": "nvarchar",  "nullable": "YES", "max_length": 100},
        {"column": "regStateName",                  "type": "nvarchar",  "nullable": "YES", "max_length": 100},
        {"column": "regdistrictName",               "type": "nvarchar",  "nullable": "YES", "max_length": 100},
        {"column": "regcityVillageTownName",        "type": "nvarchar",  "nullable": "YES", "max_length": 100},
        {"column": "otherCustType",                 "type": "nvarchar",  "nullable": "YES", "max_length": 100},
        {"column": "legacy_batch_id",               "type": "bigint",    "nullable": "YES", "max_length": None},
        {"column": "legacy_report_id",              "type": "bigint",    "nullable": "YES", "max_length": None},
        {"column": "migrated_flag",                 "type": "char",      "nullable": "YES", "max_length": 1},
        {"column": "legacy_re_id",                  "type": "nvarchar",  "nullable": "YES", "max_length": 20},
        {"column": "job id ",                       "type": "nvarchar",  "nullable": "YES", "max_length": 20},
        {"column": "rcd_create date",               "type": "datetime2", "nullable": "YES", "max_length": None},
        {"column": "rcd_update_date",               "type": "datetime2", "nullable": "YES", "max_length": None},
        {"column": "LEGACY_NATUREOFBUSINESS",       "type": "varchar",   "nullable": "YES", "max_length": 60},
        {"column": "UNIQUECOMPANYIDNUMBER",         "type": "varchar",   "nullable": "YES", "max_length": 50},
        {"column": "identifierNonAvailability",     "type": "nvarchar",  "nullable": "YES", "max_length": 50},
        {"column": "kycFormatCode",                 "type": "nvarchar",  "nullable": "YES", "max_length": 10},
        {"column": "reportType",                    "type": "nvarchar",  "nullable": "YES", "max_length": 50},
        {"column": "otherIdentifierName",           "type": "nvarchar",  "nullable": "YES", "max_length": 100},
        {"column": "otherIdentifierNumber",         "type": "nvarchar",  "nullable": "YES", "max_length": 100},
        {"column": "individualDetailsNotAvailable", "type": "nvarchar",  "nullable": "YES", "max_length": 5},
        {"column": "soleProprietorFirm",            "type": "varchar",   "nullable": "YES", "max_length": 255},
        {"column": "ucicOwnerOfSoleProprietorFirm", "type": "varchar",   "nullable": "YES", "max_length": 255},
        {"column": "nameOwnerOfSoleProprietorFirm", "type": "nvarchar",  "nullable": "YES", "max_length": 302},
        {"column": "primaryEntity",                 "type": "nvarchar",  "nullable": "YES", "max_length": 5},
    ],

    # "fingate_AnotherTable": [ ... ],
}

# ── Per-table DB schema qualifiers ────────────────────────────────────────────
TABLE_QUALIFIERS: dict[str, str] = {
    "fingate_CbwtrBank": "FINCORE_BRIDGE",
    "fingate_Gos":       "FINCORE_BRIDGE",
    "finnet_Currency":   "FIUMetaHub",
    "finnet_Country":    "FIUMetaHub",
    "fingate_KycSummary":    "FINCORE_BRIDGE",
    "fingate_AccountPerson": "FINCORE_BRIDGE",
    "fingate_AccountDetail": "FINCORE_BRIDGE",
    "fingate_EntityDetail":  "FINCORE_BRIDGE",
    # "fingate_NextTable": "FINCORE_BRIDGE",
}

# Fallback qualifier if a table isn't listed above
DEFAULT_QUALIFIER = "FINCORE_BRIDGE"

# Keep this for backward compat with schema_to_ddl calls that pass schema_qualifier
SCHEMA_QUALIFIER = None  


# ══════════════════════════════════════════════════════════════════════════════
#  METADATA — business meaning for every column (used by the prompt + indexing)
# ══════════════════════════════════════════════════════════════════════════════

COLUMN_META: dict[str, dict] = {

    # ── fingate_CbwtrBank ─────────────────────────────────────────────────────

    "fingate_CbwtrBank.transactionId": {
        "alias":       "transaction ID",
        "description": "Unique identifier for each cross-border wire transaction",
        "tags":        ["id", "transaction", "wire", "unique key"],
    },
    "fingate_CbwtrBank.transactionDate": {
        "alias":       "transaction date",
        "description": "Date and time when the wire transaction was initiated",
        "tags":        ["date", "when", "timestamp", "time"],
    },
    "fingate_CbwtrBank.trasactionTime": {   # note: typo in original DDL preserved
        "alias":       "transaction time",
        "description": "Time component of the transaction (separate from date)",
        "tags":        ["time", "hour", "when"],
    },
    "fingate_CbwtrBank.txCurrencyCode": {
        "alias":       "transaction currency code",
        "description": "Numeric code representing the original foreign currency of the transaction",
        "tags":        ["currency", "forex", "code"],
    },
    "fingate_CbwtrBank.amountInInr": {
        "alias":       "amount in INR",
        "description": "Transaction amount converted to Indian Rupees",
        "tags":        ["amount", "value", "rupee", "INR", "money"],
    },
    "fingate_CbwtrBank.amountInTxCurrency": {
        "alias":       "amount in original currency",
        "description": "Transaction amount in the original foreign currency before conversion",
        "tags":        ["amount", "value", "foreign", "currency", "money"],
    },
    "fingate_CbwtrBank.originCountry": {
        "alias":       "origin country",
        "description": "Numeric code of the country where the transaction originated",
        "tags":        ["country", "origin", "source", "from"],
    },
    "fingate_CbwtrBank.institution": {
        "alias":       "reporting institution",
        "description": "Name of the bank or financial institution that reported this transaction",
        "tags":        ["bank", "institution", "reporter", "entity"],
    },
    "fingate_CbwtrBank.destinationCountry": {
        "alias":       "destination country",
        "description": "Numeric code of the country where funds are being sent",
        "tags":        ["country", "destination", "to", "target", "receiving country"],
    },
    "fingate_CbwtrBank.senderName": {
        "alias":       "sender name / originator name",
        "description": "Full name of the person or entity sending the wire",
        "tags":        ["sender", "originator", "remitter", "name", "who sent"],
    },
    "fingate_CbwtrBank.indentifierType": {
        "alias":       "sender identifier type",
        "description": "Type of identity document used to identify the sender (e.g. passport, PAN)",
        "tags":        ["identifier", "KYC", "document", "sender", "ID type"],
    },
    "fingate_CbwtrBank.senderIdentifierAcNo": {
        "alias":       "sender identifier / account number",
        "description": "Sender's account number or identity document number",
        "tags":        ["account", "sender", "identifier", "account number"],
    },
    "fingate_CbwtrBank.senderBankOrBic": {
        "alias":       "sender bank / BIC code",
        "description": "BIC/SWIFT code or name of the sender's bank",
        "tags":        ["bank", "BIC", "SWIFT", "sender", "sending bank"],
    },
    "fingate_CbwtrBank.senderAddressLine1": {
        "alias":       "sender address",
        "description": "Street address of the sender",
        "tags":        ["address", "sender", "location", "street"],
    },
    "fingate_CbwtrBank.senderCountry": {
        "alias":       "sender country",
        "description": "Numeric code of the sender's country of residence",
        "tags":        ["country", "sender", "from", "residence"],
    },
    "fingate_CbwtrBank.senderPinCode": {
        "alias":       "sender PIN / postal code",
        "description": "Postal or PIN code of the sender's address",
        "tags":        ["pin", "postal", "zip", "sender", "address"],
    },
    "fingate_CbwtrBank.senderLocality": {
        "alias":       "sender locality",
        "description": "Locality or neighbourhood of the sender's address",
        "tags":        ["locality", "area", "sender", "address"],
    },
    "fingate_CbwtrBank.senderState": {
        "alias":       "sender state",
        "description": "Numeric code for the Indian state of the sender",
        "tags":        ["state", "sender", "address", "India"],
    },
    "fingate_CbwtrBank.senderDistrict": {
        "alias":       "sender district",
        "description": "Numeric code for the district of the sender's address",
        "tags":        ["district", "sender", "address"],
    },
    "fingate_CbwtrBank.senderCityVillageTown": {
        "alias":       "sender city / village / town",
        "description": "Numeric code for the city, village, or town of the sender",
        "tags":        ["city", "town", "village", "sender", "address"],
    },
    "fingate_CbwtrBank.benificiaryName": {
        "alias":       "beneficiary name (legacy field)",
        "description": "Name of the beneficiary — older field, may duplicate beneficiaryBankOrBic data",
        "tags":        ["beneficiary", "receiver", "name", "recipient"],
    },
    "fingate_CbwtrBank.benificiaryBankOrBic": {
        "alias":       "beneficiary bank / BIC (legacy field)",
        "description": "BIC/SWIFT code of the beneficiary's bank — older field",
        "tags":        ["bank", "BIC", "SWIFT", "beneficiary", "receiving bank"],
    },
    "fingate_CbwtrBank.beneficiaryBankOrBic": {
        "alias":       "beneficiary bank / BIC code",
        "description": "BIC/SWIFT code or name of the beneficiary's bank",
        "tags":        ["bank", "BIC", "SWIFT", "beneficiary", "receiving bank"],
    },
    "fingate_CbwtrBank.beneficiaryAcNo": {
        "alias":       "beneficiary account number",
        "description": "Account number of the beneficiary receiving the wire",
        "tags":        ["account", "beneficiary", "receiver", "account number"],
    },
    "fingate_CbwtrBank.beneficiaryIdentifierType": {
        "alias":       "beneficiary identifier type",
        "description": "Type of identity document used to identify the beneficiary",
        "tags":        ["identifier", "KYC", "beneficiary", "document type"],
    },
    "fingate_CbwtrBank.beneficiaryIdentifierAcNo": {
        "alias":       "beneficiary identifier / account number",
        "description": "Beneficiary's identity document number or account number",
        "tags":        ["identifier", "account", "beneficiary", "KYC"],
    },
    "fingate_CbwtrBank.benAddressLine1": {
        "alias":       "beneficiary address",
        "description": "Street address of the beneficiary",
        "tags":        ["address", "beneficiary", "receiver", "street"],
    },
    "fingate_CbwtrBank.benCountry": {
        "alias":       "beneficiary country",
        "description": "Numeric code of the beneficiary's country",
        "tags":        ["country", "beneficiary", "receiving country", "destination"],
    },
    "fingate_CbwtrBank.benPinCode": {
        "alias":       "beneficiary PIN / postal code",
        "description": "Postal code of the beneficiary's address",
        "tags":        ["pin", "postal", "beneficiary", "address"],
    },
    "fingate_CbwtrBank.benLocality": {
        "alias":       "beneficiary locality",
        "description": "Locality or neighbourhood of the beneficiary's address",
        "tags":        ["locality", "area", "beneficiary", "address"],
    },
    "fingate_CbwtrBank.benState": {
        "alias":       "beneficiary state",
        "description": "Numeric code for the state of the beneficiary",
        "tags":        ["state", "beneficiary", "address"],
    },
    "fingate_CbwtrBank.benDistrict": {
        "alias":       "beneficiary district",
        "description": "Numeric code for the district of the beneficiary's address",
        "tags":        ["district", "beneficiary", "address"],
    },
    "fingate_CbwtrBank.benCityVillageTown": {
        "alias":       "beneficiary city / village / town",
        "description": "Numeric code for the city or town of the beneficiary",
        "tags":        ["city", "town", "village", "beneficiary", "address"],
    },
    "fingate_CbwtrBank.rbiCode": {
        "alias":       "RBI code",
        "description": "Reserve Bank of India assigned code for the reporting entity",
        "tags":        ["RBI", "regulator", "code", "India", "central bank"],
    },
    "fingate_CbwtrBank.swiftMessageText": {
        "alias":       "SWIFT message text",
        "description": "Full raw SWIFT message body associated with the transaction",
        "tags":        ["SWIFT", "message", "raw", "MT103", "wire details"],
    },
    "fingate_CbwtrBank.swiftMessageCode": {
        "alias":       "SWIFT message type code",
        "description": "SWIFT message type (e.g. MT103 for single customer credit transfer)",
        "tags":        ["SWIFT", "MT103", "message type", "code"],
    },
    "fingate_CbwtrBank.senderCorresBankOrBic": {
        "alias":       "sender correspondent bank / BIC",
        "description": "BIC of the correspondent bank on the sender's side",
        "tags":        ["correspondent", "bank", "BIC", "SWIFT", "sender", "intermediary"],
    },
    "fingate_CbwtrBank.beneficiaryCorresBankOrBic": {
        "alias":       "beneficiary correspondent bank / BIC",
        "description": "BIC of the correspondent bank on the beneficiary's side",
        "tags":        ["correspondent", "bank", "BIC", "beneficiary", "intermediary"],
    },
    "fingate_CbwtrBank.thirdReimInstBankOrBic": {
        "alias":       "third reimbursement institution BIC",
        "description": "BIC of the third reimbursement institution in the payment chain",
        "tags":        ["reimbursement", "third party", "BIC", "correspondent"],
    },
    "fingate_CbwtrBank.intermediaryInstBankOrBic": {
        "alias":       "intermediary institution BIC",
        "description": "BIC of the intermediary institution routing the payment",
        "tags":        ["intermediary", "routing", "BIC", "SWIFT", "bank"],
    },
    "fingate_CbwtrBank.reportId": {
        "alias":       "report ID",
        "description": "ID linking this transaction to its parent STR/CTR report",
        "tags":        ["report", "STR", "CTR", "filing", "ID"],
    },
    "fingate_CbwtrBank.batchId": {
        "alias":       "batch ID",
        "description": "ID of the data ingestion batch this transaction was loaded with",
        "tags":        ["batch", "ingestion", "load", "ETL"],
    },

    # ── fingate_Gos ───────────────────────────────────────────────────────────

    "fingate_Gos.reportId": {
        "alias":       "report ID",
        "description": "Links this GOS record to its parent STR/CTR report",
        "tags":        ["report", "STR", "CTR", "ID", "link"],
    },
    "fingate_Gos.batchId": {
        "alias":       "batch ID",
        "description": "Data ingestion batch this GOS record was loaded with",
        "tags":        ["batch", "ETL", "ingestion", "load"],
    },
    "fingate_Gos.kycFundSource": {
        "alias":       "KYC fund source",
        "description": "Source of funds as declared during KYC — where the money came from",
        "tags":        ["KYC", "source of funds", "AML", "due diligence"],
    },
    "fingate_Gos.kycFundDestination": {
        "alias":       "KYC fund destination",
        "description": "Intended destination of funds as declared during KYC",
        "tags":        ["KYC", "destination of funds", "AML", "due diligence"],
    },
    "fingate_Gos.gosTag1": {
        "alias":       "GOS tag 1 (offence category code)",
        "description": "Numeric code for the primary offence/predicate category in the GOS filing",
        "tags":        ["offence", "category", "GOS", "predicate", "crime type"],
    },
    "fingate_Gos.gosTag2": {
        "alias":       "GOS tag 2 (sub-category)",
        "description": "Sub-category or secondary classification tag for the GOS offence",
        "tags":        ["offence", "sub-category", "GOS", "classification"],
    },
    "fingate_Gos.gosTag3": {
        "alias":       "GOS tag 3",
        "description": "Tertiary classification tag for the GOS offence",
        "tags":        ["GOS", "tag", "classification"],
    },
    "fingate_Gos.gosTextNarration": {
        "alias":       "GOS narration / free text",
        "description": "Full free-text narrative describing the suspicious activity in the GOS",
        "tags":        ["narration", "description", "free text", "GOS", "suspicious activity"],
    },
    "fingate_Gos.gosTag4": {
        "alias":       "GOS tag 4",
        "description": "Additional classification tag for the GOS offence",
        "tags":        ["GOS", "tag", "classification"],
    },
    "fingate_Gos.otherOffenceType": {
        "alias":       "other offence type",
        "description": "Free-text description of offence type when it doesn't fit standard categories",
        "tags":        ["offence", "crime", "other", "manual"],
    },
    "fingate_Gos.status": {
        "alias":       "GOS status code",
        "description": "Numeric status of the GOS record (e.g. draft, submitted, approved)",
        "tags":        ["status", "workflow", "approval", "state"],
    },
    "fingate_Gos.statusByUserId": {
        "alias":       "status changed by user ID",
        "description": "ID of the user who last changed the GOS status",
        "tags":        ["user", "status", "audit", "who"],
    },
    "fingate_Gos.statusByUserName": {
        "alias":       "status changed by username",
        "description": "Username of the analyst who last changed the GOS status",
        "tags":        ["user", "analyst", "status", "audit", "name"],
    },
    "fingate_Gos.statusDate": {
        "alias":       "status change date",
        "description": "Date and time when the GOS status was last updated",
        "tags":        ["date", "status", "when", "timestamp", "audit"],
    },
    "fingate_Gos.statusComment": {
        "alias":       "status comment / remarks",
        "description": "Reviewer or analyst comment at the time of status change",
        "tags":        ["comment", "remark", "note", "reviewer", "audit"],
    },
    "fingate_Gos.legacy_batch_id": {
        "alias":       "legacy batch ID",
        "description": "Batch ID from the legacy system before migration",
        "tags":        ["legacy", "batch", "migration", "old system"],
    },
    "fingate_Gos.legacy_report_id": {
        "alias":       "legacy report ID",
        "description": "Report ID from the legacy system before migration",
        "tags":        ["legacy", "report", "migration", "old system"],
    },
    "fingate_Gos.migrated_flag": {
        "alias":       "migrated flag",
        "description": "Y/N flag indicating whether this record was migrated from a legacy system",
        "tags":        ["migration", "flag", "legacy", "Y/N"],
    },
    "fingate_Gos.legacy_re_id": {
        "alias":       "legacy reporting entity ID",
        "description": "Reporting entity ID from the legacy system",
        "tags":        ["legacy", "reporting entity", "RE", "ID"],
    },
    "fingate_Gos.job_id": {
        "alias":       "job ID",
        "description": "ETL or processing job ID that created or updated this record",
        "tags":        ["job", "ETL", "pipeline", "processing"],
    },
    "fingate_Gos.otherRedFlagInd": {
        "alias":       "other red flag indicators",
        "description": "Free-text or coded list of additional AML red flag indicators",
        "tags":        ["red flag", "AML", "indicator", "alert", "suspicious"],
    },
    "fingate_Gos.attemptedTransaction": {
        "alias":       "attempted transaction flag",
        "description": "Y/N — whether this was an attempted (not completed) transaction",
        "tags":        ["attempted", "flag", "incomplete", "Y/N"],
    },
    "fingate_Gos.trasactionNotAvailable": {
        "alias":       "transaction not available flag",
        "description": "Y/N — whether transaction details were unavailable at time of filing",
        "tags":        ["not available", "missing", "flag", "Y/N"],
    },

    # ── finnet_Currency ───────────────────────────────────────────────────────

    "finnet_Currency.id_": {
        "alias":       "currency record ID",
        "description": "Primary key / internal ID of the currency record",
        "tags":        ["ID", "primary key", "currency"],
    },
    "finnet_Currency.countryName": {
        "alias":       "country name",
        "description": "Full name of the country associated with this currency",
        "tags":        ["country", "name", "currency", "lookup"],
    },
    "finnet_Currency.currencyCode": {
        "alias":       "currency code (ISO 4217)",
        "description": "ISO 4217 alphabetic currency code, e.g. USD, EUR, INR",
        "tags":        ["currency", "ISO", "code", "forex", "lookup"],
    },
    "finnet_Currency.description": {
        "alias":       "currency description",
        "description": "Human-readable description or full name of the currency",
        "tags":        ["currency", "description", "name", "label"],
    },
    "finnet_Currency.name": {
        "alias":       "currency name",
        "description": "Short name of the currency (e.g. US Dollar, Euro)",
        "tags":        ["currency", "name", "label"],
    },
    "finnet_Currency.countryCode": {
        "alias":       "country code",
        "description": "Short country code associated with this currency (ISO 3166 alpha-2 or similar)",
        "tags":        ["country", "code", "ISO", "lookup"],
    },

    # ── finnet_Country ────────────────────────────────────────────────────────

    "finnet_Country.id_": {
        "alias":       "country record ID",
        "description": "Primary key / internal numeric ID of the country record",
        "tags":        ["ID", "primary key", "country"],
    },
    "finnet_Country.name": {
        "alias":       "country name",
        "description": "Full official name of the country",
        "tags":        ["country", "name", "lookup"],
    },
    "finnet_Country.countryCode": {
        "alias":       "country code",
        "description": "Short country code used internally (may be numeric or alpha)",
        "tags":        ["country", "code", "lookup"],
    },
    "finnet_Country.isoCode": {
        "alias":       "ISO country code",
        "description": "ISO 3166-1 alpha-2 or alpha-3 country code (e.g. IN, US, CN)",
        "tags":        ["ISO", "country", "code", "standard", "lookup"],
    },
    "finnet_Country.callCode": {
        "alias":       "international dialling code",
        "description": "International telephone dialling code for the country (e.g. +91 for India)",
        "tags":        ["call code", "dial", "phone", "country", "ISD"],
    },
    "finnet_Country.endDate": {
        "alias":       "record end date",
        "description": "Date after which this country record is no longer active (soft-delete / SCD)",
        "tags":        ["end date", "active", "expired", "SCD", "validity"],
    },


    # ── fingate_KycSummary ────────────────────────────────────────────────────

    "fingate_KycSummary.primaryEntity": {
        "alias":       "primary entity flag",
        "description": "Flag (Y/N/NA) marking whether this KYC record represents the primary subject entity in the STR filing. Aligns with FinCEN SAR Part I principal subject designation.",
        "tags":        ["primary entity", "SAR subject", "principal", "FinCEN Part I", "STR subject"],
    },
    "fingate_KycSummary.customer": {
        "alias":       "customer reference / UCIC",
        "description": "Internal customer reference or UCIC linking this KYC summary to the bank's CIF/customer master. Mandated under RBI KYC Master Circular for unique identification.",
        "tags":        ["customer", "UCIC", "CIF", "RBI KYC", "customer reference", "identification"],
    },
    "fingate_KycSummary.entityType": {
        "alias":       "entity type (individual / corporate / trust)",
        "description": "Legal form of the subject — individual, proprietary firm, partnership, company, trust, NGO etc. Required under FATF R.10 and PMLA CDD rules for risk-stratified due diligence.",
        "tags":        ["entity type", "legal form", "individual", "corporate", "trust", "FATF R.10", "CDD", "PMLA"],
    },
    "fingate_KycSummary.entityName": {
        "alias":       "entity / customer name",
        "description": "Full legal name of the customer or entity as per KYC documents (passport, PAN card, certificate of incorporation). FinCEN SAR Part I Item 4 equivalent.",
        "tags":        ["name", "entity name", "customer name", "legal name", "KYC", "FinCEN Part I Item 4"],
    },
    "fingate_KycSummary.UCICID": {
        "alias":       "UCIC — Unique Customer Identification Code",
        "description": "RBI-mandated Unique Customer Identification Code assigned to every customer. Enables holistic view of customer across products and branches; feeds into centralised KYC registry (CKYCRR).",
        "tags":        ["UCIC", "unique customer ID", "RBI KYC circular", "CKYCRR", "centralised KYC", "customer ID"],
    },
    "fingate_KycSummary.PAN": {
        "alias":       "PAN — Permanent Account Number",
        "description": "10-character alphanumeric PAN issued by Income Tax Department. Mandatory for transactions above INR 50,000 per PMLA Rule 9; cross-referenced with CBDT for tax-evasion red flags.",
        "tags":        ["PAN", "Permanent Account Number", "Income Tax", "CBDT", "PMLA Rule 9", "tax identifier", "KYC OVD"],
    },
    "fingate_KycSummary.uniqueID": {
        "alias":       "unique identifier (Aadhaar / passport / driving licence)",
        "description": "Officially Valid Document (OVD) number used for identity verification. Per RBI KYC Master Circular OVDs include Aadhaar, passport, driving licence, voter ID, NREGA card.",
        "tags":        ["OVD", "Aadhaar", "passport", "driving licence", "voter ID", "identity proof", "KYC verification", "RBI OVD list"],
    },
    "fingate_KycSummary.risk": {
        "alias":       "customer risk rating (Low / Medium / High)",
        "description": "Risk-based classification of the customer per FATF R.10 and RBI risk-based KYC. High-risk customers include PEPs, correspondent banks, and customers from FATF greylisted jurisdictions.",
        "tags":        ["risk rating", "Low", "Medium", "High", "risk-based KYC", "FATF R.10", "PEP", "EDD", "CDD risk category"],
    },
    "fingate_KycSummary.profession": {
        "alias":       "occupation / profession / nature of business",
        "description": "Customer's stated occupation or business activity. Used for source-of-funds plausibility and typology-matching per FATF R.10 CDD. High-risk occupations include bullion dealers, real estate agents, casino operators.",
        "tags":        ["occupation", "profession", "business", "source of funds", "CDD", "FATF R.10", "typology", "DNFBP", "nature of business"],
    },
    "fingate_KycSummary.incomePerYear": {
        "alias":       "declared annual income",
        "description": "Customer's self-declared annual income used to benchmark transaction volumes. Significant deviation triggers EDD per FATF R.10 and RBI KYC guidelines on ongoing monitoring.",
        "tags":        ["income", "annual income", "declared income", "source of funds", "EDD", "transaction monitoring", "KYC baseline"],
    },
    "fingate_KycSummary.reportId": {
        "alias":       "report ID (STR/CTR filing link)",
        "description": "Foreign key linking this KYC summary to the parent STR or CTR report filed with FIU-IND via FINgate 2.0. Equivalent to FinCEN SAR Document Control Number (DCN).",
        "tags":        ["report ID", "STR", "CTR", "FIU-IND", "FINgate", "DCN", "filing link", "BSA ID"],
    },
    "fingate_KycSummary.status": {
        "alias":       "workflow status code",
        "description": "Numeric code representing the review/approval state of this KYC record (e.g. 1=Draft, 2=Submitted, 3=Approved, 4=Rejected). Tracks the STR workflow lifecycle in FINgate.",
        "tags":        ["status", "workflow", "approval", "draft", "submitted", "FINgate workflow"],
    },
    "fingate_KycSummary.statusByUserId":  {"alias": "status changed by user ID", "description": "Internal user ID of the compliance analyst who last updated the record status — audit trail for PMLA record-keeping.", "tags": ["audit trail", "user ID", "PMLA record keeping", "compliance officer"]},
    "fingate_KycSummary.statusByUserName":{"alias": "status changed by username", "description": "Username of the compliance officer who last changed status — part of mandatory five-year audit trail under PMLA Section 12.", "tags": ["audit trail", "username", "PMLA Section 12", "compliance officer", "reviewer"]},
    "fingate_KycSummary.statusDate":      {"alias": "status change timestamp", "description": "Datetime of last status change. PMLA mandates five-year record retention from filing date.", "tags": ["timestamp", "status date", "PMLA retention", "audit"]},
    "fingate_KycSummary.statusComment":   {"alias": "reviewer comment / disposition note", "description": "Free-text disposition comment by the reviewing officer explaining the status decision.", "tags": ["comment", "disposition", "reviewer note", "audit"]},
    "fingate_KycSummary.legacy_batch_id": {"alias": "legacy batch ID (pre-migration)", "description": "Batch ID from legacy FINnet/FINgate 1.x system before migration to FINgate 2.0.", "tags": ["legacy", "batch", "FINnet", "migration", "FINgate 1.x"]},
    "fingate_KycSummary.legacy_report_id":{"alias": "legacy report ID (pre-migration)", "description": "Report ID from legacy system prior to FINgate 2.0 migration.", "tags": ["legacy", "report", "migration", "FINgate 1.x"]},
    "fingate_KycSummary.migrated_flag":   {"alias": "migration flag (Y/N)", "description": "Y if record was migrated from legacy FINnet system; N if natively created in FINgate 2.0.", "tags": ["migration", "FINnet", "FINgate", "legacy flag", "Y/N"]},
    "fingate_KycSummary.legacy_re_id":    {"alias": "legacy reporting entity ID", "description": "Reporting entity identifier from legacy system.", "tags": ["legacy", "reporting entity", "RE code"]},
    "fingate_KycSummary.rcd_create_date": {"alias": "record creation timestamp", "description": "Datetime this KYC record was first created in FINgate.", "tags": ["created", "timestamp", "ETL", "audit"]},
    "fingate_KycSummary.BATCHID":         {"alias": "ingestion batch ID", "description": "ETL batch under which this record was loaded into FINgate.", "tags": ["batch", "ETL", "ingestion"]},
    "fingate_KycSummary.REPORTDATASETID": {"alias": "report dataset ID", "description": "Groups all records belonging to the same report submission dataset.", "tags": ["dataset", "report group", "submission"]},
    "fingate_KycSummary.REPORTREFERENCENO":{"alias": "report reference number", "description": "Human-readable reference number of the STR/CTR report as assigned by the reporting institution.", "tags": ["reference number", "STR ref", "CTR ref", "report number", "institution reference"]},

    # ── fingate_AccountPerson ─────────────────────────────────────────────────

    "fingate_AccountPerson.accountNo": {
        "alias":       "account number",
        "description": "Bank account number to which this person relationship is linked. Core identifier for account-based STR/CTR filings per FinCEN SAR Part III and FIU-IND CBWT reporting.",
        "tags":        ["account number", "bank account", "FinCEN Part III", "STR account", "account link"],
    },
    "fingate_AccountPerson.relationTypeId": {
        "alias":       "relationship type code (account holder / authorized signatory / UBO)",
        "description": "Numeric lookup code for how this person is related to the account — e.g. primary holder, joint holder, authorized signatory, power of attorney, UBO. Relevant to FATF R.24 beneficial ownership.",
        "tags":        ["relationship type", "account holder", "joint holder", "signatory", "UBO", "power of attorney", "FATF R.24", "beneficial ownership"],
    },
    "fingate_AccountPerson.personType": {
        "alias":       "person type (customer / non-customer / walk-in)",
        "description": "Classifies the person as an existing KYC-verified customer, a non-customer (walk-in), or an entity representative. Non-customers trigger enhanced CDD under FATF R.10.",
        "tags":        ["person type", "customer", "non-customer", "walk-in", "CDD", "FATF R.10", "identity verification"],
    },
    "fingate_AccountPerson.ucic": {
        "alias":       "UCIC — Unique Customer Identification Code",
        "description": "RBI UCIC of the linked person. Null for non-customers (walk-ins). Used to JOIN with fingate_KycSummary and fingate_EntityDetail for full KYC profile.",
        "tags":        ["UCIC", "RBI KYC", "customer ID", "JOIN key", "non-customer NULL"],
    },
    "fingate_AccountPerson.reportId":        {"alias": "report ID", "description": "Links to the parent STR/CTR report in FINgate.", "tags": ["report", "STR", "CTR", "FIU-IND", "link"]},
    "fingate_AccountPerson.nonCustomerName": {
        "alias":       "non-customer name (walk-in / third party)",
        "description": "Name of a non-KYC-verified person (walk-in or third-party) associated with the account. Populated only when personType indicates non-customer; triggers CDD gap in AML review.",
        "tags":        ["non-customer", "walk-in", "third party", "name", "CDD gap", "anonymous transaction risk"],
    },
    "fingate_AccountPerson.batchId":         {"alias": "batch ID", "description": "ETL ingestion batch.", "tags": ["batch", "ETL"]},
    "fingate_AccountPerson.reportDataSetId": {"alias": "report dataset ID", "description": "Groups records in the same filing dataset.", "tags": ["dataset", "filing group"]},
    "fingate_AccountPerson.legacy_batch_id": {"alias": "legacy batch ID", "description": "Batch ID from pre-FINgate 2.0 system.", "tags": ["legacy", "migration"]},
    "fingate_AccountPerson.legacy_report_id":{"alias": "legacy report ID", "description": "Report ID from pre-FINgate 2.0 system.", "tags": ["legacy", "migration"]},
    "fingate_AccountPerson.migrated_flag":   {"alias": "migration flag (Y/N)", "description": "Y if migrated from legacy FINnet.", "tags": ["legacy", "migration", "Y/N"]},
    "fingate_AccountPerson.legacy_re_id":    {"alias": "legacy reporting entity ID", "description": "RE code from legacy system.", "tags": ["legacy", "RE code"]},
    "fingate_AccountPerson.reportRefNo": {
        "alias":       "report reference number",
        "description": "Institution-assigned reference number of the associated STR/CTR report.",
        "tags":        ["report reference", "STR ref", "CTR ref", "institution reference"],
    },
    "fingate_AccountPerson.reportType": {
        "alias":       "report type (STR / CTR / NTR / CBWT)",
        "description": "Type of regulatory report: STR (Suspicious Transaction Report), CTR (Cash Transaction Report), NTR (Non-Profit Transaction Report), or CBWT (Cross-Border Wire Transfer). Determines applicable FIU-IND reporting threshold and format.",
        "tags":        ["report type", "STR", "CTR", "NTR", "CBWT", "FIU-IND", "regulatory report", "filing type"],
    },

    # ── fingate_AccountDetail ─────────────────────────────────────────────────

    "fingate_AccountDetail.batchId":     {"alias": "batch ID", "description": "ETL ingestion batch for this account record.", "tags": ["batch", "ETL", "ingestion"]},
    "fingate_AccountDetail.reportId":    {"alias": "report ID", "description": "Links to the parent STR/CTR filing in FINgate.", "tags": ["report", "STR", "CTR", "FIU-IND"]},
    "fingate_AccountDetail.accountType": {
        "alias":       "account type code (savings / current / NRE / NRO / FCNR)",
        "description": "Numeric lookup code for the type of bank account. Key for AML typology — NRE/NRO/FCNR accounts have cross-border fund flow implications under FEMA; current accounts are higher-risk for structuring.",
        "tags":        ["account type", "savings", "current", "NRE", "NRO", "FCNR", "FEMA", "structuring", "account classification"],
    },
    "fingate_AccountDetail.accountNumber": {
        "alias":       "account number",
        "description": "Bank account number as reported to FIU-IND. Primary JOIN key to fingate_AccountPerson and fingate_CbwtrBank wire transactions.",
        "tags":        ["account number", "bank account", "JOIN key", "CBWT", "wire", "FIU-IND"],
    },
    "fingate_AccountDetail.branchCode": {
        "alias":       "branch code (RBI / internal)",
        "description": "Branch identifier code. Cross-referenced with RBI branch master to identify geographic concentration of suspicious activity.",
        "tags":        ["branch code", "branch", "RBI branch master", "geographic concentration", "location"],
    },
    "fingate_AccountDetail.acOpeningDate": {
        "alias":       "account opening date",
        "description": "Date the account was opened. Short-lived accounts opened just before large suspicious transactions are a key AML typology indicator (FATF ML typologies report).",
        "tags":        ["account opening", "date opened", "new account", "AML typology", "FATF ML typology", "short-lived account"],
    },
    "fingate_AccountDetail.acClosingDate": {
        "alias":       "account closing date",
        "description": "Date the account was closed. Accounts closed soon after suspicious activity may indicate layering — a core ML stage per FATF.",
        "tags":        ["account closing", "closed account", "layering", "FATF ML stages", "exit after suspicious activity"],
    },
    "fingate_AccountDetail.accountStatus": {
        "alias":       "account status (active / dormant / frozen / closed)",
        "description": "Current operational status of the account. Dormant accounts suddenly active with large transactions are a red flag per RBI KYC circular on dormant accounts.",
        "tags":        ["account status", "active", "dormant", "frozen", "closed", "dormant account red flag", "RBI KYC circular"],
    },
    "fingate_AccountDetail.status":          {"alias": "workflow status code", "description": "FINgate review workflow status of this account record.", "tags": ["workflow", "status", "review"]},
    "fingate_AccountDetail.statusByUserId":  {"alias": "status changed by user ID", "description": "Compliance officer user ID — part of PMLA audit trail.", "tags": ["audit trail", "user ID", "PMLA"]},
    "fingate_AccountDetail.statusByUserName":{"alias": "status changed by username", "description": "Compliance officer username.", "tags": ["audit", "username", "reviewer"]},
    "fingate_AccountDetail.statusDate":      {"alias": "status change date", "description": "Datetime of last status change.", "tags": ["timestamp", "audit"]},
    "fingate_AccountDetail.statusComment":   {"alias": "reviewer disposition comment", "description": "Free-text comment by reviewing officer.", "tags": ["comment", "disposition", "audit"]},
    "fingate_AccountDetail.legacy_batch_id": {"alias": "legacy batch ID", "description": "Pre-FINgate 2.0 batch ID.", "tags": ["legacy", "migration"]},
    "fingate_AccountDetail.legacy_report_id":{"alias": "legacy report ID", "description": "Pre-FINgate 2.0 report ID.", "tags": ["legacy", "migration"]},
    "fingate_AccountDetail.migrated_flag":   {"alias": "migration flag (Y/N)", "description": "Y if migrated from FINnet.", "tags": ["migration", "Y/N"]},
    "fingate_AccountDetail.legacy_re_id":    {"alias": "legacy reporting entity ID", "description": "RE code from legacy system.", "tags": ["legacy", "RE"]},
    "fingate_AccountDetail.job_id":          {"alias": "ETL job ID", "description": "Processing job that created or updated this record.", "tags": ["ETL", "job", "pipeline"]},
    "fingate_AccountDetail.rcd_create_date": {"alias": "record creation timestamp", "description": "Datetime this record was first created in FINgate.", "tags": ["created", "timestamp", "audit"]},
    "fingate_AccountDetail.rcd_upd d_update_date": {"alias": "record last updated timestamp", "description": "Datetime of most recent update. Note: column name has a typo (space) preserved from DDL.", "tags": ["updated", "timestamp", "audit", "DDL typo"]},
    "fingate_AccountDetail.noofCashTxn": {
        "alias":       "number of cash transactions",
        "description": "Count of cash transactions on this account in the reporting period. High cash transaction counts are a primary CTR trigger (>INR 10L/day per PMLA) and structuring indicator.",
        "tags":        ["cash transactions", "count", "CTR trigger", "structuring", "PMLA threshold", "cash intensity"],
    },
    "fingate_AccountDetail.noofCredits": {
        "alias":       "number of credit entries",
        "description": "Total credit count for the account in the report period. Rapid layering often shows high credit counts from multiple sources per FATF layering typology.",
        "tags":        ["credits", "credit count", "layering", "FATF typology", "placement"],
    },
    "fingate_AccountDetail.noofDebits": {
        "alias":       "number of debit entries",
        "description": "Total debit count. High debit frequency relative to credits may indicate integration-stage ML activity.",
        "tags":        ["debits", "debit count", "integration", "FATF ML stages"],
    },
    "fingate_AccountDetail.reasonActFreeze": {
        "alias":       "reason for account freeze",
        "description": "Regulatory or legal reason why the account was frozen — e.g. court order, ED attachment under PMLA Section 17, OFAC/UN sanctions designation.",
        "tags":        ["freeze", "account freeze", "ED attachment", "PMLA Section 17", "sanctions", "OFAC", "UN sanctions", "court order"],
    },
    "fingate_AccountDetail.totalCashDeposit": {
        "alias":       "total cash deposit amount",
        "description": "Aggregate cash deposited on the account in the period. Primary CTR calculation field; amounts exceeding INR 10L/day mandatory under PMLA Rule 3.",
        "tags":        ["cash deposit", "total cash", "CTR", "PMLA Rule 3", "INR 10 lakh", "structuring threshold"],
    },
    "fingate_AccountDetail.totalCashTxAmt": {
        "alias":       "total cash transaction amount",
        "description": "Total value of all cash transactions (deposits + withdrawals). Used to identify structuring below CTR threshold (smurfing).",
        "tags":        ["cash total", "cash transaction amount", "structuring", "smurfing", "CTR avoidance"],
    },
    "fingate_AccountDetail.totalCreditAmount": {
        "alias":       "total credit amount",
        "description": "Sum of all credit entries. Compared against declared income (fingate_KycSummary.incomePerYear) to identify unexplained wealth — a key STR trigger.",
        "tags":        ["total credits", "credit amount", "unexplained wealth", "income mismatch", "STR trigger", "EDD"],
    },
    "fingate_AccountDetail.totalDebitAmt": {
        "alias":       "total debit amount",
        "description": "Sum of all debit entries. Large outflows to high-risk jurisdictions shortly after inflows indicate layering.",
        "tags":        ["total debits", "debit amount", "outflow", "layering", "high-risk jurisdiction"],
    },
    "fingate_AccountDetail.reportRefNo":  {"alias": "report reference number", "description": "Institution-assigned STR/CTR reference number.", "tags": ["report reference", "STR", "CTR"]},
    "fingate_AccountDetail.reportType":   {"alias": "report type (STR/CTR/NTR/CBWT)", "description": "Regulatory report type filed with FIU-IND.", "tags": ["STR", "CTR", "NTR", "CBWT", "report type"]},

    # ── fingate_EntityDetail ──────────────────────────────────────────────────

    "fingate_EntityDetail.ucic": {
        "alias":       "UCIC — Unique Customer Identification Code",
        "description": "RBI-mandated UCIC linking this entity to its centralised KYC record. Primary JOIN key across fingate_KycSummary, fingate_AccountPerson, and fingate_AccountDetail.",
        "tags":        ["UCIC", "RBI KYC", "customer ID", "JOIN key", "CKYCRR", "CIF"],
    },
    "fingate_EntityDetail.name": {
        "alias":       "entity / company name",
        "description": "Full legal name of the entity as per CDD documents — MOA, certificate of incorporation, or GSTIN registration. Matches FinCEN SAR Part I entity name field.",
        "tags":        ["entity name", "company name", "legal name", "CDD", "MOA", "FinCEN Part I"],
    },
    "fingate_EntityDetail.uniqueCompanyId": {
        "alias":       "CIN — Company Identification Number (MCA)",
        "description": "21-character Corporate Identity Number issued by Ministry of Corporate Affairs (MCA21). Used to verify legal existence and detect shell companies per FATF R.24 beneficial ownership transparency.",
        "tags":        ["CIN", "MCA", "MCA21", "company registration", "shell company detection", "FATF R.24", "beneficial ownership"],
    },
    "fingate_EntityDetail.pan": {
        "alias":       "PAN — Permanent Account Number (entity)",
        "description": "10-character PAN of the entity for tax identity verification. Cross-checked with CBDT data for tax compliance and unexplained wealth detection. Mandatory under PMLA Rule 9.",
        "tags":        ["PAN", "Income Tax", "CBDT", "entity PAN", "PMLA Rule 9", "tax identity", "KYC OVD"],
    },
    "fingate_EntityDetail.panAvailability": {
        "alias":       "PAN availability flag (Y/N/NA)",
        "description": "Indicates whether PAN was furnished (Y), not available (N), or not applicable (NA). Missing PAN for a company is a KYC deficiency red flag under RBI CDD norms.",
        "tags":        ["PAN availability", "KYC deficiency", "missing PAN", "CDD gap", "RBI norms"],
    },
    "fingate_EntityDetail.tan": {
        "alias":       "TAN — Tax Deduction Account Number",
        "description": "10-character TAN issued by Income Tax Dept for entities deducting TDS at source. Presence confirms entity is an active business; absence for companies claiming business income is suspicious.",
        "tags":        ["TAN", "TDS", "Tax Deduction", "Income Tax", "business verification", "entity legitimacy"],
    },
    "fingate_EntityDetail.gstin": {
        "alias":       "GSTIN — GST Identification Number",
        "description": "15-character GSTIN for GST-registered businesses. Cross-referenced with GSTN portal to verify turnover consistency with account activity. High turnover + low GSTIN filing = typology for trade-based ML.",
        "tags":        ["GSTIN", "GST", "GSTN", "turnover verification", "trade-based money laundering", "TBML", "tax compliance"],
    },
    "fingate_EntityDetail.iec": {
        "alias":       "IEC — Importer Exporter Code (DGFT)",
        "description": "10-digit IEC issued by DGFT for entities engaged in import/export. Critical for CBWT analysis — all cross-border wire transfers for trade must reference a valid IEC. Missing IEC for a claimed trade company is a TBML red flag.",
        "tags":        ["IEC", "DGFT", "import export", "trade finance", "CBWT", "TBML", "trade-based ML", "cross-border trade"],
    },
    "fingate_EntityDetail.iecAvailability": {
        "alias":       "IEC availability flag (Y/N/NA)",
        "description": "Whether IEC was furnished. Missing IEC for an entity claiming trade-based remittances is a primary TBML typology indicator per FATF ML through trade.",
        "tags":        ["IEC availability", "TBML", "trade", "missing IEC", "FATF trade ML typology"],
    },
    "fingate_EntityDetail.pekrn": {
        "alias":       "PEKRN — PEP / Existing KYC Reference Number",
        "description": "Reference number for Politically Exposed Person (PEP) status or existing KYC record. PEPs require enhanced due diligence (EDD) under FATF R.12 and RBI KYC Master Circular Chapter VI.",
        "tags":        ["PEKRN", "PEP", "politically exposed person", "EDD", "FATF R.12", "RBI KYC Chapter VI", "high-risk customer"],
    },
    "fingate_EntityDetail.telephoneNumber":  {"alias": "telephone number", "description": "Registered telephone number of the entity for contact verification.", "tags": ["telephone", "contact", "CDD", "verification"]},
    "fingate_EntityDetail.mobileNumber":     {"alias": "mobile number", "description": "Mobile number for OTP-based verification and contact.", "tags": ["mobile", "OTP", "contact", "CDD"]},
    "fingate_EntityDetail.emailId":          {"alias": "email address", "description": "Registered email address for entity communications and e-KYC.", "tags": ["email", "contact", "e-KYC", "CDD"]},
    "fingate_EntityDetail.companyWebsite":   {"alias": "company website", "description": "Official website URL. Verified during CDD to confirm legitimate business presence.", "tags": ["website", "online presence", "CDD", "business verification"]},
    "fingate_EntityDetail.addressLine1":     {"alias": "registered address line 1", "description": "Primary street address of the entity's operating premises.", "tags": ["address", "registered address", "premises", "CDD"]},
    "fingate_EntityDetail.locality":         {"alias": "locality / area", "description": "Locality or neighbourhood of the operating address.", "tags": ["locality", "area", "address", "geography"]},
    "fingate_EntityDetail.country": {
        "alias":       "country of operation (lookup code)",
        "description": "Numeric foreign key to finnet_Country. Identifies the country of the entity's operating address. Non-Indian entities with Indian accounts trigger FEMA/RBI cross-border scrutiny.",
        "tags":        ["country", "operating country", "foreign entity", "FEMA", "finnet_Country FK", "cross-border"],
    },
    "fingate_EntityDetail.pinCode":          {"alias": "PIN / postal code", "description": "Postal code of operating address.", "tags": ["PIN", "postal code", "address"]},
    "fingate_EntityDetail.state":            {"alias": "state code (operating address)", "description": "Numeric state code of operating address.", "tags": ["state", "address", "geography"]},
    "fingate_EntityDetail.district":         {"alias": "district code (operating address)", "description": "Numeric district code.", "tags": ["district", "address", "geography"]},
    "fingate_EntityDetail.cityVillageTown":  {"alias": "city / village / town code", "description": "Numeric city or town code for the operating address.", "tags": ["city", "town", "village", "address"]},
    "fingate_EntityDetail.linesOfBusiness": {
        "alias":       "lines of business / nature of business (NIC code)",
        "description": "Description of the entity's business activities. Cross-matched against NIC (National Industrial Classification) codes. Shell companies typically list vague or atypical business activities.",
        "tags":        ["nature of business", "NIC code", "industry", "shell company", "business activity", "CDD", "KYB"],
    },
    "fingate_EntityDetail.fcraStatus": {
        "alias":       "FCRA registration status (Y/N/NA)",
        "description": "Whether the entity is registered under Foreign Contribution (Regulation) Act 2010. FCRA-registered NGOs and trusts can receive foreign funds; unregistered entities receiving foreign wires are a high-risk typology (NTR trigger for FIU-IND).",
        "tags":        ["FCRA", "Foreign Contribution Act", "NGO", "trust", "NTR", "foreign funds", "FIU-IND NTR", "high-risk entity"],
    },
    "fingate_EntityDetail.fcraRegState":    {"alias": "FCRA registration state", "description": "State in which FCRA registration was obtained.", "tags": ["FCRA", "state", "NGO registration"]},
    "fingate_EntityDetail.fcraRegNumber":   {"alias": "FCRA registration number", "description": "FCRA certificate number issued by Ministry of Home Affairs.", "tags": ["FCRA number", "MHA", "NGO", "foreign contribution"]},
    "fingate_EntityDetail.regAddress":      {"alias": "registered office address", "description": "Statutory registered office address as per MCA/ROC filings. May differ from operating address — discrepancy is a shell company indicator.", "tags": ["registered office", "MCA", "ROC", "statutory address", "shell company"]},
    "fingate_EntityDetail.regLocality":     {"alias": "registered address locality", "description": "Locality of registered office.", "tags": ["registered address", "locality"]},
    "fingate_EntityDetail.regCountry":      {"alias": "country of registered office (lookup code)", "description": "Numeric FK to finnet_Country for the registered office country.", "tags": ["registered country", "finnet_Country FK", "incorporation country"]},
    "fingate_EntityDetail.regPinCode":      {"alias": "registered office PIN code", "description": "Postal code of registered office.", "tags": ["PIN", "registered address"]},
    "fingate_EntityDetail.regState":        {"alias": "registered office state code", "description": "State of registered office.", "tags": ["state", "registered office"]},
    "fingate_EntityDetail.regDistrict":     {"alias": "registered office district code", "description": "District of registered office.", "tags": ["district", "registered office"]},
    "fingate_EntityDetail.regCityVillageTown": {"alias": "registered office city / town code", "description": "City or town of registered office.", "tags": ["city", "town", "registered office"]},
    "fingate_EntityDetail.dateOfInc": {
        "alias":       "date of incorporation",
        "description": "Date the company was incorporated per MCA/ROC records. Very recently incorporated companies filing large CBWT transactions are a shell company red flag (FATF R.24).",
        "tags":        ["incorporation date", "date of incorporation", "MCA", "ROC", "shell company", "FATF R.24", "newly formed entity"],
    },
    "fingate_EntityDetail.customerType": {
        "alias":       "customer type code (individual/company/trust/NGO/PEP)",
        "description": "Numeric lookup classifying the customer category. Drives which CDD tier applies: standard CDD for individuals, enhanced CDD for companies, EDD for PEPs and high-risk categories per FATF R.10.",
        "tags":        ["customer type", "individual", "company", "trust", "NGO", "PEP", "CDD tier", "FATF R.10", "EDD"],
    },
    "fingate_EntityDetail.lastkycDate": {
        "alias":       "last KYC refresh date",
        "description": "Date KYC documents were last updated. RBI mandates periodic KYC refresh: high-risk customers every 2 years, medium-risk every 8 years, low-risk every 10 years. Overdue KYC is a compliance violation.",
        "tags":        ["KYC refresh", "periodic KYC", "RBI KYC schedule", "high-risk 2yr", "medium-risk 8yr", "low-risk 10yr", "KYC expiry"],
    },
    "fingate_EntityDetail.onboardingDate": {
        "alias":       "customer onboarding date",
        "description": "Date the customer relationship was established. Combined with transaction history, used to detect anomalous early activity in new accounts.",
        "tags":        ["onboarding", "customer since", "account opening", "new customer", "early suspicious activity"],
    },
    "fingate_EntityDetail.customerRiskLevel": {
        "alias":       "customer risk level (Low / Medium / High / Very High)",
        "description": "Composite risk rating assigned during CDD. High/Very High triggers EDD, enhanced transaction monitoring, and senior management approval per FATF R.10 and RBI risk-based KYC.",
        "tags":        ["risk level", "CDD risk", "EDD trigger", "FATF R.10", "RBI risk-based KYC", "PEP risk", "high-risk customer"],
    },
    "fingate_EntityDetail.ubo": {
        "alias":       "UBO — Ultimate Beneficial Owner name",
        "description": "Name of the natural person who ultimately owns or controls the entity (25%+ shareholding or effective control). Mandatory disclosure under FATF R.24 and Companies Act 2013 Section 90 (significant beneficial ownership).",
        "tags":        ["UBO", "ultimate beneficial owner", "beneficial owner", "FATF R.24", "Companies Act Section 90", "SBO", "shell company", "ownership chain"],
    },
    "fingate_EntityDetail.uboAvailability": {
        "alias":       "UBO availability / disclosure status",
        "description": "Whether UBO information was disclosed, not available, or not applicable. Non-disclosure of UBO for a company is a major red flag per FATF R.24 — indicates potential use of nominee shareholders or shell company structuring.",
        "tags":        ["UBO disclosure", "beneficial ownership transparency", "FATF R.24", "nominee shareholders", "shell company", "opacity"],
    },
    "fingate_EntityDetail.reportId":         {"alias": "report ID", "description": "Parent STR/CTR report in FINgate.", "tags": ["report", "STR", "CTR", "FIU-IND"]},
    "fingate_EntityDetail.batchId":          {"alias": "batch ID", "description": "ETL ingestion batch.", "tags": ["batch", "ETL"]},
    "fingate_EntityDetail.reportDataSetId":  {"alias": "report dataset ID", "description": "Groups records in same filing dataset.", "tags": ["dataset", "filing"]},
    "fingate_EntityDetail.status":           {"alias": "workflow status code", "description": "FINgate review workflow status.", "tags": ["workflow", "status"]},
    "fingate_EntityDetail.statusByUserId":   {"alias": "status changed by user ID", "description": "Compliance officer user ID — PMLA audit trail.", "tags": ["audit", "user ID", "PMLA"]},
    "fingate_EntityDetail.statusByUserName": {"alias": "status changed by username", "description": "Compliance officer username.", "tags": ["audit", "username"]},
    "fingate_EntityDetail.statusDate":       {"alias": "status change timestamp", "description": "Datetime of last status change.", "tags": ["timestamp", "audit"]},
    "fingate_EntityDetail.statusComment":    {"alias": "reviewer comment", "description": "Free-text disposition note.", "tags": ["comment", "disposition"]},
    "fingate_EntityDetail.stateName":        {"alias": "state name (operating address)", "description": "Resolved state name for operating address.", "tags": ["state", "geography", "address"]},
    "fingate_EntityDetail.districtName":     {"alias": "district name (operating address)", "description": "Resolved district name.", "tags": ["district", "geography"]},
    "fingate_EntityDetail.cityVillageTownName": {"alias": "city / town name (operating address)", "description": "Resolved city or town name.", "tags": ["city", "town", "geography"]},
    "fingate_EntityDetail.regStateName":     {"alias": "state name (registered office)", "description": "Resolved state name for registered office.", "tags": ["state", "registered office"]},
    "fingate_EntityDetail.regdistrictName":  {"alias": "district name (registered office)", "description": "Resolved district name for registered office.", "tags": ["district", "registered office"]},
    "fingate_EntityDetail.regcityVillageTownName": {"alias": "city / town name (registered office)", "description": "Resolved city or town name for registered office.", "tags": ["city", "town", "registered office"]},
    "fingate_EntityDetail.otherCustType":    {"alias": "other customer type (free text)", "description": "Free-text override when customerType does not fit standard lookup values.", "tags": ["customer type", "other", "free text"]},
    "fingate_EntityDetail.legacy_batch_id":  {"alias": "legacy batch ID", "description": "Pre-FINgate 2.0 batch ID.", "tags": ["legacy", "migration"]},
    "fingate_EntityDetail.legacy_report_id": {"alias": "legacy report ID", "description": "Pre-FINgate 2.0 report ID.", "tags": ["legacy", "migration"]},
    "fingate_EntityDetail.migrated_flag":    {"alias": "migration flag (Y/N)", "description": "Y if migrated from FINnet.", "tags": ["migration", "Y/N"]},
    "fingate_EntityDetail.legacy_re_id":     {"alias": "legacy reporting entity ID", "description": "RE code from legacy system.", "tags": ["legacy", "RE code"]},
    "fingate_EntityDetail.job id ":          {"alias": "ETL job ID", "description": "Processing job ID — note: column name has a space (DDL typo preserved).", "tags": ["ETL", "job", "DDL typo"]},
    "fingate_EntityDetail.rcd_create date":  {"alias": "record creation timestamp", "description": "Datetime record was first created — note: column name has a space (DDL typo preserved).", "tags": ["created", "timestamp", "DDL typo"]},
    "fingate_EntityDetail.rcd_update_date":  {"alias": "record last updated timestamp", "description": "Datetime of most recent update.", "tags": ["updated", "timestamp"]},
    "fingate_EntityDetail.LEGACY_NATUREOFBUSINESS": {
        "alias":       "legacy nature of business (NIC description)",
        "description": "Free-text business description from legacy system, often containing NIC (National Industrial Classification) code description. Used for continuity during migration.",
        "tags":        ["nature of business", "NIC", "legacy", "industry description", "migration"],
    },
    "fingate_EntityDetail.UNIQUECOMPANYIDNUMBER": {
        "alias":       "unique company ID number (legacy CIN/LLPIN)",
        "description": "Legacy field storing CIN or LLPIN (Limited Liability Partnership Identification Number). Superseded by uniqueCompanyId in current schema.",
        "tags":        ["CIN", "LLPIN", "company ID", "legacy", "MCA"],
    },
    "fingate_EntityDetail.identifierNonAvailability": {
        "alias":       "reason for missing identifier",
        "description": "Explanation when a mandatory identifier (PAN, IEC, GSTIN) is unavailable. Documents the CDD exemption basis per RBI simplified KYC norms.",
        "tags":        ["missing identifier", "KYC exemption", "simplified KYC", "RBI norms", "CDD gap reason"],
    },
    "fingate_EntityDetail.kycFormatCode": {
        "alias":       "KYC format code (FINgate KYC form version)",
        "description": "Code identifying which FIU-IND KYC reporting format version was used for this entity's KYC data capture.",
        "tags":        ["KYC format", "FIU-IND format", "reporting format", "FINgate version"],
    },
    "fingate_EntityDetail.reportType":   {"alias": "report type (STR/CTR/NTR/CBWT)", "description": "Type of regulatory report filed with FIU-IND.", "tags": ["STR", "CTR", "NTR", "CBWT"]},
    "fingate_EntityDetail.otherIdentifierName": {
        "alias":       "other identifier type name",
        "description": "Name of a non-standard identifier type (e.g. SEBI registration, IRDA licence) when standard fields don't cover the entity category.",
        "tags":        ["identifier type", "SEBI", "IRDA", "other ID", "non-standard", "CDD"],
    },
    "fingate_EntityDetail.otherIdentifierNumber": {
        "alias":       "other identifier number",
        "description": "Number corresponding to the non-standard identifier named in otherIdentifierName.",
        "tags":        ["identifier number", "SEBI reg no", "IRDA no", "other ID value"],
    },
    "fingate_EntityDetail.individualDetailsNotAvailable": {
        "alias":       "individual details not available flag (Y/N)",
        "description": "Y if individual-level KYC details could not be obtained (e.g. for trust beneficiaries or shell-company UBOs). A Y here combined with high transaction value is a strong EDD trigger per FATF R.24.",
        "tags":        ["missing individual details", "KYC gap", "FATF R.24", "EDD trigger", "trust beneficiary", "UBO unknown"],
    },
    "fingate_EntityDetail.soleProprietorFirm": {
        "alias":       "sole proprietor firm name",
        "description": "Name of the proprietary firm when the customer is a sole proprietor. Sole proprietorships are a common vehicle for structuring cash deposits under PMLA.",
        "tags":        ["sole proprietor", "proprietary firm", "structuring", "PMLA", "cash deposits", "small business"],
    },
    "fingate_EntityDetail.ucicOwnerOfSoleProprietorFirm": {
        "alias":       "UCIC of sole proprietor owner",
        "description": "UCIC of the individual who owns the sole proprietor firm. Links the firm's transactions back to the individual's KYC profile for holistic AML monitoring.",
        "tags":        ["UCIC", "sole proprietor owner", "individual KYC", "AML monitoring", "entity linking"],
    },
    "fingate_EntityDetail.nameOwnerOfSoleProprietorFirm": {
        "alias":       "name of sole proprietor owner",
        "description": "Full name of the individual owner of the sole proprietor firm. Used to detect name-variant matching and alias detection in STR investigations.",
        "tags":        ["owner name", "sole proprietor", "alias detection", "name matching", "STR investigation"],
    },
    "fingate_EntityDetail.primaryEntity": {
        "alias":       "primary entity flag",
        "description": "Flag indicating if this entity is the primary subject of the STR/CTR filing versus a related party or counterpart.",
        "tags":        ["primary entity", "STR subject", "primary vs related party", "filing subject"],
    },

    # ── Add metadata for remaining tables below in the same format ────────────
}


# ══════════════════════════════════════════════════════════════════════════════
#  HELPERS  (used by pipeline and app)
# ══════════════════════════════════════════════════════════════════════════════

def get_all_tables() -> list[str]:
    return list(SCHEMA.keys())


def get_qualifier(table: str) -> str:
    """Return the SQL Server schema prefix for a given table."""
    return TABLE_QUALIFIERS.get(table, DEFAULT_QUALIFIER)


def get_inline_comments(table: str) -> dict[str, str]:
    """
    Returns {table.column: alias} for schema_to_ddl inline comment injection.
    Only includes columns that have metadata defined.
    """
    out = {}
    for col in SCHEMA.get(table, []):
        key = f"{table}.{col['column']}"
        if key in COLUMN_META:
            out[key] = COLUMN_META[key]["alias"]
    return out


def get_qualified_table(table: str) -> str:
    """Returns [QUALIFIER].[table] using the per-table qualifier map."""
    q = get_qualifier(table)
    return f"[{q}].[{table}]"


def build_glossary_block(tables: list[str] | None = None) -> str:
    """
    Auto-generate a compact glossary block from COLUMN_META.
    Injected into the LLM prompt so it understands plain-English → column mapping.

    Parameters
    ----------
    tables  Restrict the glossary to these tables. None → all tables.
            Scoping this to the user's selected tables keeps the model from
            referencing tables that aren't in the provided DDL / allowlist.
    """
    allowed = set(tables) if tables is not None else None
    lines = ["-- AUTO-GENERATED COLUMN GLOSSARY --"]
    current_table = None
    for key, meta in COLUMN_META.items():
        table, col = key.split(".", 1)
        if allowed is not None and table not in allowed:
            continue
        if table != current_table:
            qualified = get_qualified_table(table)
            lines.append(f"\n-- {qualified}")
            current_table = table
        lines.append(f"  '{meta['alias']}' → {col}  ({meta['description'][:60]})")
    return "\n".join(lines)
