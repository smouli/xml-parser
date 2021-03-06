CREATE TABLE public.LongBusiness
				(
				repno TEXT PRIMARY KEY,
				CompanyName TEXT,
				IRSNo TEXT,
				CIKNo TEXT,
				IssueID INT,
				IssueType TEXT,
				IssueDesc TEXT,
				IssueOrder TEXT,
				IssueName TEXT,
				Ticker TEXT,
				CUSIP TEXT,
				ISIN TEXT,
				RIC TEXT,
				SEDOL TEXT,
				DisplayRIC TEXT,
				InstrumentPI TEXT,
				QuotePI TEXT,
				CoStatus TEXT,
				CoStatusCode TEXT,
				CoType TEXT,
				CoTypeCode TEXT,
				LastModified TEXT,
				LatestAvailableAnnual TEXT,
				LatestAvailableInterim TEXT,
				ReportingCurrency TEXT,
				ReportingCurrencyCode TEXT,
				MostRecentExchange TEXT,
				MostRecentExchangeDate TEXT,
				Industry TEXT,
				IndustryType TEXT,
				IndustryCode TEXT,
				IndustryMnem TEXT,
				Sector TEXT,
				SectorType TEXT,
				SectorCode TEXT,
				SectorMnem TEXT
				)

3:43 PM	CREATE UNIQUE INDEX LongBusiness_repno_uindex ON public.LongBusiness (repno)

