CREATE TABLE IF NOT EXISTS public.pay
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    username character varying(50) COLLATE pg_catalog."default" NOT NULL,
    balance double precision NOT NULL,
    CONSTRAINT pay_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE public.pay
    OWNER to postgres;


INSERT INTO public.pay(
	 username, balance)
	VALUES ( 'Maga', 5000);

INSERT INTO public.pay(
	 username, balance)
	VALUES ( 'Denis', 5000);



CREATE TABLE IF NOT EXISTS public.history
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    id_from integer NOT NULL,
    id_to integer NOT NULL,
    amount double precision NOT NULL,
    CONSTRAINT history_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE public.history
    OWNER to postgres;