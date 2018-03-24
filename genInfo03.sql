
CREATE TABLE public.geninfo03
(
    repno TEXT PRIMARY KEY NOT NULL,
    companyname TEXT,
    companytype TEXT,
    taxonomytype TEXT,
    code TEXT,
    description TEXT,
    orders TEXT,
    employees TEXT,
    totalsharesout TEXT,
    totalfloat TEXT,
    commonshareholders TEXT,
    incorporatedin TEXT,
    incorporatedincountry TEXT,
    incorporatedindate TEXT,
    businesssummary TEXT,
    equitycomposition TEXT,
    analystfootnotes TEXT,
    financialsummary TEXT,
    CONSTRAINT geninfo03_geninfo03_repno_fk FOREIGN KEY (repno) REFERENCES geninfo03 (repno) ON DELETE CASCADE
);
CREATE UNIQUE INDEX geninfo03_pkey ON public.geninfo03 (repno);
CREATE UNIQUE INDEX geninfo03_repno_uindex ON public.geninfo03 (repno);