CREATE TABLE public.geninfo03_tax
				(
				taxid INT PRIMARY KEY,
				repno TEXT,
				taxonomytype TEXT,
				code TEXT,
				orders TEXT,
				CONSTRAINT geninfo03_tax_geninfo03_repno_fk FOREIGN KEY (repno) REFERENCES geninfo03 (repno) ON DELETE CASCADE ON UPDATE CASCADE
				)
CREATE UNIQUE INDEX geninfo03_tax_taxid_uindex ON public.geninfo03_tax (taxid)