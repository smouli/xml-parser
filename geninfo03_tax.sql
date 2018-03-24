CREATE TABLE public.geninfo03_tax
(
    taxid INTEGER DEFAULT nextval('geninfo03_tax_taxid_seq'::regclass) PRIMARY KEY NOT NULL,
    repno TEXT,
    taxonomytype TEXT,
    code TEXT,
    description TEXT,
    orders INTEGER
);
CREATE UNIQUE INDEX geninfo03_tax_taxid_pk ON public.geninfo03_tax (taxid);
CREATE UNIQUE INDEX geninfo03_tax_taxid_uindex ON public.geninfo03_tax (taxid);