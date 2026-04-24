--
-- PostgreSQL database dump
--

\restrict MkSYJtdGW4tUlHNJmspk02z1s6aqSuGxLafIRCxGLIsjmHj9gkg009M0iAvCpYt

-- Dumped from database version 18.3
-- Dumped by pg_dump version 18.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: categoria; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.categoria (
    id_categoria integer NOT NULL,
    nombre character varying(100) NOT NULL,
    fecha date NOT NULL,
    precios numeric(10,2) NOT NULL
);


ALTER TABLE public.categoria OWNER TO postgres;

--
-- Name: categoria_id_categoria_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.categoria_id_categoria_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.categoria_id_categoria_seq OWNER TO postgres;

--
-- Name: categoria_id_categoria_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.categoria_id_categoria_seq OWNED BY public.categoria.id_categoria;


--
-- Name: cita; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cita (
    id_cita integer NOT NULL,
    nombre_paciente character varying(100) NOT NULL,
    apellido_paciente character varying(100) NOT NULL,
    cedula character varying(20) NOT NULL,
    fecha_cita date NOT NULL,
    hora_cita time without time zone NOT NULL,
    estado character varying(20),
    motivo character varying(255),
    id_usuario integer
);


ALTER TABLE public.cita OWNER TO postgres;

--
-- Name: cita_id_cita_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.cita_id_cita_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cita_id_cita_seq OWNER TO postgres;

--
-- Name: cita_id_cita_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cita_id_cita_seq OWNED BY public.cita.id_cita;


--
-- Name: configuracion; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.configuracion (
    id integer NOT NULL,
    tasa_bcv numeric(10,4),
    ultima_actualizacion timestamp without time zone
);


ALTER TABLE public.configuracion OWNER TO postgres;

--
-- Name: configuracion_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.configuracion_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.configuracion_id_seq OWNER TO postgres;

--
-- Name: configuracion_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.configuracion_id_seq OWNED BY public.configuracion.id;


--
-- Name: facturacion; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.facturacion (
    id_factura integer NOT NULL,
    nombre_paciente character varying(150),
    id_examenes integer,
    precio_final numeric(20,2),
    fecha_facturacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    id_transaccion character varying(50),
    estado_cierre boolean DEFAULT false
);


ALTER TABLE public.facturacion OWNER TO postgres;

--
-- Name: facturacion_id_factura_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.facturacion_id_factura_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.facturacion_id_factura_seq OWNER TO postgres;

--
-- Name: facturacion_id_factura_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.facturacion_id_factura_seq OWNED BY public.facturacion.id_factura;


--
-- Name: historial_medico; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.historial_medico (
    id_historial integer NOT NULL,
    cedula character varying(20) NOT NULL,
    telefono character varying(20),
    edad integer,
    fecha_nac date,
    nombre_paciente character varying(100),
    antecedentes text,
    enfermedad_actual text,
    indicaciones text,
    observaciones text,
    altura character varying(20),
    peso character varying(20),
    tension character varying(20),
    direccion text,
    sexo character varying(10),
    fecha_registro timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    estado_cierre boolean DEFAULT false
);


ALTER TABLE public.historial_medico OWNER TO postgres;

--
-- Name: historial_medico_id_historial_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.historial_medico_id_historial_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.historial_medico_id_historial_seq OWNER TO postgres;

--
-- Name: historial_medico_id_historial_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.historial_medico_id_historial_seq OWNED BY public.historial_medico.id_historial;


--
-- Name: login; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.login (
    id_login integer NOT NULL,
    id_usuario integer,
    usuario character varying(50) NOT NULL,
    contrasena character varying(255) NOT NULL,
    fecha_sesion timestamp without time zone,
    id_rol integer,
    activo boolean DEFAULT true NOT NULL
);


ALTER TABLE public.login OWNER TO postgres;

--
-- Name: login_id_login_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.login_id_login_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.login_id_login_seq OWNER TO postgres;

--
-- Name: login_id_login_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.login_id_login_seq OWNED BY public.login.id_login;


--
-- Name: pago_detalle; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.pago_detalle (
    id_pago integer NOT NULL,
    id_transaccion character varying(50) NOT NULL,
    metodo character varying(50) NOT NULL,
    monto numeric(10,2) NOT NULL,
    fecha timestamp without time zone
);


ALTER TABLE public.pago_detalle OWNER TO postgres;

--
-- Name: pago_detalle_id_pago_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.pago_detalle_id_pago_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.pago_detalle_id_pago_seq OWNER TO postgres;

--
-- Name: pago_detalle_id_pago_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.pago_detalle_id_pago_seq OWNED BY public.pago_detalle.id_pago;


--
-- Name: rol; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rol (
    id_rol integer NOT NULL,
    nombre character varying(50) NOT NULL
);


ALTER TABLE public.rol OWNER TO postgres;

--
-- Name: rol_id_rol_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.rol_id_rol_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.rol_id_rol_seq OWNER TO postgres;

--
-- Name: rol_id_rol_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.rol_id_rol_seq OWNED BY public.rol.id_rol;


--
-- Name: sessiones; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sessiones (
    id_session integer NOT NULL,
    id_usuario integer,
    fecha date NOT NULL,
    hora time without time zone NOT NULL,
    acciones text
);


ALTER TABLE public.sessiones OWNER TO postgres;

--
-- Name: sessiones_id_session_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.sessiones_id_session_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sessiones_id_session_seq OWNER TO postgres;

--
-- Name: sessiones_id_session_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.sessiones_id_session_seq OWNED BY public.sessiones.id_session;


--
-- Name: tabla_citas; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tabla_citas (
    id_citas integer NOT NULL,
    nombres character varying(100) NOT NULL,
    apellidos character varying(100) NOT NULL,
    motivo text,
    fecha timestamp without time zone NOT NULL,
    id_bot_sic bigint,
    cedula character varying(20),
    estado character varying(20) DEFAULT 'Pendiente'::character varying
);


ALTER TABLE public.tabla_citas OWNER TO postgres;

--
-- Name: tabla_citas_id_citas_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tabla_citas_id_citas_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tabla_citas_id_citas_seq OWNER TO postgres;

--
-- Name: tabla_citas_id_citas_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tabla_citas_id_citas_seq OWNED BY public.tabla_citas.id_citas;


--
-- Name: tabla_examenes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tabla_examenes (
    id_examenes integer NOT NULL,
    nombre_examen character varying(150) NOT NULL,
    descripcion text,
    id_categoria integer,
    precio numeric(10,2) DEFAULT 0.00,
    categoria character varying(50)
);


ALTER TABLE public.tabla_examenes OWNER TO postgres;

--
-- Name: tabla_examenes_id_examenes_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tabla_examenes_id_examenes_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tabla_examenes_id_examenes_seq OWNER TO postgres;

--
-- Name: tabla_examenes_id_examenes_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tabla_examenes_id_examenes_seq OWNED BY public.tabla_examenes.id_examenes;


--
-- Name: usuario; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.usuario (
    id_usuario integer NOT NULL,
    correo_electronico character varying(100) NOT NULL,
    nombres character varying(100) NOT NULL,
    apellidos character varying(100) NOT NULL,
    fecha date NOT NULL
);


ALTER TABLE public.usuario OWNER TO postgres;

--
-- Name: usuario_id_usuario_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.usuario_id_usuario_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.usuario_id_usuario_seq OWNER TO postgres;

--
-- Name: usuario_id_usuario_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.usuario_id_usuario_seq OWNED BY public.usuario.id_usuario;


--
-- Name: categoria id_categoria; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categoria ALTER COLUMN id_categoria SET DEFAULT nextval('public.categoria_id_categoria_seq'::regclass);


--
-- Name: cita id_cita; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cita ALTER COLUMN id_cita SET DEFAULT nextval('public.cita_id_cita_seq'::regclass);


--
-- Name: configuracion id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.configuracion ALTER COLUMN id SET DEFAULT nextval('public.configuracion_id_seq'::regclass);


--
-- Name: facturacion id_factura; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.facturacion ALTER COLUMN id_factura SET DEFAULT nextval('public.facturacion_id_factura_seq'::regclass);


--
-- Name: historial_medico id_historial; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.historial_medico ALTER COLUMN id_historial SET DEFAULT nextval('public.historial_medico_id_historial_seq'::regclass);


--
-- Name: login id_login; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.login ALTER COLUMN id_login SET DEFAULT nextval('public.login_id_login_seq'::regclass);


--
-- Name: pago_detalle id_pago; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pago_detalle ALTER COLUMN id_pago SET DEFAULT nextval('public.pago_detalle_id_pago_seq'::regclass);


--
-- Name: rol id_rol; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rol ALTER COLUMN id_rol SET DEFAULT nextval('public.rol_id_rol_seq'::regclass);


--
-- Name: sessiones id_session; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sessiones ALTER COLUMN id_session SET DEFAULT nextval('public.sessiones_id_session_seq'::regclass);


--
-- Name: tabla_citas id_citas; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tabla_citas ALTER COLUMN id_citas SET DEFAULT nextval('public.tabla_citas_id_citas_seq'::regclass);


--
-- Name: tabla_examenes id_examenes; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tabla_examenes ALTER COLUMN id_examenes SET DEFAULT nextval('public.tabla_examenes_id_examenes_seq'::regclass);


--
-- Name: usuario id_usuario; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario ALTER COLUMN id_usuario SET DEFAULT nextval('public.usuario_id_usuario_seq'::regclass);


--
-- Data for Name: categoria; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.categoria (id_categoria, nombre, fecha, precios) FROM stdin;
12	Pediatria	2026-04-17	0.00
13	Urologia	2026-04-17	0.00
14	Dermatologia	2026-04-17	0.00
15	Cirugia	2026-04-17	0.00
\.


--
-- Data for Name: cita; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.cita (id_cita, nombre_paciente, apellido_paciente, cedula, fecha_cita, hora_cita, estado, motivo, id_usuario) FROM stdin;
2	bryant bueno	jjjjjjj	30821491	2026-04-17	22:09:00	Pendiente	jsjsjsjsjs	\N
\.


--
-- Data for Name: configuracion; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.configuracion (id, tasa_bcv, ultima_actualizacion) FROM stdin;
1	481.2177	2026-04-20 08:37:28.10258
\.


--
-- Data for Name: facturacion; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.facturacion (id_factura, nombre_paciente, id_examenes, precio_final, fecha_facturacion, id_transaccion, estado_cierre) FROM stdin;
36	Miriam Sarahi Aguilera Serrano	20	12030.44	2026-04-17 23:42:33.914841	9F31E771	t
37	Bryant Bueno	20	12030.44	2026-04-19 09:21:26.499996	80542394	t
38	Miriam Sarahi Aguilera Serrano	21	14436.53	2026-04-19 09:21:49.821558	E3E4A6AA	t
39	bryant bueno	20	12030.44	2026-04-19 12:46:32.475564	2CE32CA1	t
40	Isum Alumno	13	12030.44	2026-04-19 13:13:51.819335	368A0194	t
41	Bryant Bueno	14	14436.53	2026-04-19 19:27:02.227311	FA157910	t
42	Bryant Bueno	20	12030.44	2026-04-19 23:13:42.089845	B0965C2E	t
\.


--
-- Data for Name: historial_medico; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.historial_medico (id_historial, cedula, telefono, edad, fecha_nac, nombre_paciente, antecedentes, enfermedad_actual, indicaciones, observaciones, altura, peso, tension, direccion, sexo, fecha_registro, estado_cierre) FROM stdin;
22	70534610	3318773054	18	\N	Miriam Sarahi Aguilera Serrano	\N	\N	\N	\N	\N	\N	\N	\N	\N	2026-04-17 23:04:28.447641	t
28	30821491	04241608958	20	\N	Bryant Bueno	\N	\N	\N	\N	\N	\N	\N	\N	\N	2026-04-20 08:13:05.351719	f
29	30370329	04123691998	22	\N	Henry Ruiz	\N	\N	\N	\N	\N	\N	\N	\N	\N	2026-04-20 08:57:59.249168	f
30	73737737	04241608958	20	\N	Kenely Hernández	\N	\N	\N	\N	\N	\N	\N	\N	\N	2026-04-20 09:40:50.371764	f
31	11410409	04141976042	57	\N	María Eugenia Oropeza	\N	\N	\N	\N	\N	\N	\N	\N	\N	2026-04-20 10:05:53.148092	f
32	25214460	04266660932	29	\N	Jose Avilan	\N	\N	\N	\N	\N	\N	\N	\N	\N	2026-04-20 10:06:01.844173	f
33	31316850	04127012278	23	\N	Kristhina Mantilla	\N	\N	\N	\N	\N	\N	\N	\N	\N	2026-04-20 10:06:18.060879	f
34	14955722	04143260944	44	\N	Angel Barrientos	\N	\N	\N	\N	\N	\N	\N	\N	\N	2026-04-20 10:06:29.373219	f
\.


--
-- Data for Name: login; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.login (id_login, id_usuario, usuario, contrasena, fecha_sesion, id_rol, activo) FROM stdin;
4	3	admin1	admin123	\N	1	t
6	11	bryant123	1234	\N	3	t
5	10	kenely	12345	\N	2	t
\.


--
-- Data for Name: pago_detalle; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.pago_detalle (id_pago, id_transaccion, metodo, monto, fecha) FROM stdin;
25	9F31E771	Divisa	9624.35	2026-04-17 23:42:33.920786
26	9F31E771	Bolivares	2500.00	2026-04-17 23:42:33.920791
27	9F31E771	Bolivares (Vuelto)	-93.91	2026-04-17 23:42:33.920793
28	80542394	Divisa	12030.44	2026-04-19 09:21:26.517856
29	E3E4A6AA	Divisa	14436.53	2026-04-19 09:21:49.825385
30	2CE32CA1	Divisa	9624.35	2026-04-19 12:46:32.502054
31	2CE32CA1	Bolivares	2450.00	2026-04-19 12:46:32.502061
32	2CE32CA1	Bolivares (Vuelto)	-43.91	2026-04-19 12:46:32.502065
33	368A0194	Divisa	9624.35	2026-04-19 13:13:51.831752
34	368A0194	Debito	3000.00	2026-04-19 13:13:51.831757
35	368A0194	Bolivares (Vuelto)	-593.91	2026-04-19 13:13:51.831759
36	FA157910	Divisa	14436.53	2026-04-19 19:27:02.244267
37	B0965C2E	Divisa	9624.35	2026-04-19 23:13:42.103267
38	B0965C2E	Bolivares	2406.00	2026-04-19 23:13:42.103272
39	B0965C2E	Debito	0.09	2026-04-19 23:13:42.103274
\.


--
-- Data for Name: rol; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.rol (id_rol, nombre) FROM stdin;
1	Administrador
2	Secretaria
3	Doctor
\.


--
-- Data for Name: sessiones; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.sessiones (id_session, id_usuario, fecha, hora, acciones) FROM stdin;
\.


--
-- Data for Name: tabla_citas; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tabla_citas (id_citas, nombres, apellidos, motivo, fecha, id_bot_sic, cedula, estado) FROM stdin;
33	Bryant	Bueno	No sé bro	2026-04-18 22:00:00	6878067708	30821491	Cancelada
38	Bryant	Bueno	Fiebre	2026-04-20 10:00:00	6878067708	30821491	Confirmada
39	Henry	Ruiz	Dolor de cabeza	2026-08-19 17:00:00	5242623699	30370329	Pendiente
40	Kenely	Hernández	Fiebre alta	2026-04-20 11:00:00	6878067708	73737737	Pendiente
43	Kristhina	Mantilla	Seguimiento anual	2026-06-21 17:00:00	1945395573	31316850	Cancelada
41	Jose	Avilan	Alergia	2026-04-20 09:30:00	1341267413	25214460	Confirmada
44	Angel	Barrientos	Dolor de cabeza	2026-04-21 10:00:00	1835412181	14955722	Confirmada
42	María	Eugenia Oropeza	Fascitis plantar bilateral	2026-04-22 17:00:00	6878067708	11410409	Confirmada
\.


--
-- Data for Name: tabla_examenes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tabla_examenes (id_examenes, nombre_examen, descripcion, id_categoria, precio, categoria) FROM stdin;
12	Hematologia Completa		12	30.00	\N
13	Examen de Orina y Heces		12	25.00	\N
14	Glicemia y Perfil Lipidico		12	30.00	\N
15	Rayos X de edad Osea		12	30.00	\N
16	Perfil Preoperatorio		15	25.00	\N
17	Ecografia Abdominal o de Partes		15	25.00	\N
18	Tomografia Axial Computarizada		15	45.00	\N
19	Urocultivo		13	30.00	\N
20	Antigeno Prostatico Especifico 		13	25.00	\N
21	Ecografia Renal y Prostatica		13	30.00	\N
22	Espermatograma		13	40.00	\N
23	Biopsia de Piel 		14	20.00	\N
24	Cultivo de Lesiones		14	25.00	\N
25	Pruebas de Alergia		14	50.00	\N
\.


--
-- Data for Name: usuario; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.usuario (id_usuario, correo_electronico, nombres, apellidos, fecha) FROM stdin;
3	admin1@sic.com	Luis	Martinez	1988-11-05
10	bryantbueno222@gmail.com	bryant 	bueno	2026-04-12
11	bryant@gmail.com	bryant	bueno	2026-04-17
\.


--
-- Name: categoria_id_categoria_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.categoria_id_categoria_seq', 15, true);


--
-- Name: cita_id_cita_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cita_id_cita_seq', 2, true);


--
-- Name: configuracion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.configuracion_id_seq', 1, true);


--
-- Name: facturacion_id_factura_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.facturacion_id_factura_seq', 42, true);


--
-- Name: historial_medico_id_historial_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.historial_medico_id_historial_seq', 34, true);


--
-- Name: login_id_login_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.login_id_login_seq', 6, true);


--
-- Name: pago_detalle_id_pago_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.pago_detalle_id_pago_seq', 39, true);


--
-- Name: rol_id_rol_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.rol_id_rol_seq', 6, true);


--
-- Name: sessiones_id_session_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.sessiones_id_session_seq', 1, true);


--
-- Name: tabla_citas_id_citas_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tabla_citas_id_citas_seq', 44, true);


--
-- Name: tabla_examenes_id_examenes_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tabla_examenes_id_examenes_seq', 26, true);


--
-- Name: usuario_id_usuario_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.usuario_id_usuario_seq', 11, true);


--
-- Name: categoria categoria_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categoria
    ADD CONSTRAINT categoria_pkey PRIMARY KEY (id_categoria);


--
-- Name: cita cita_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cita
    ADD CONSTRAINT cita_pkey PRIMARY KEY (id_cita);


--
-- Name: configuracion configuracion_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.configuracion
    ADD CONSTRAINT configuracion_pkey PRIMARY KEY (id);


--
-- Name: facturacion facturacion_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.facturacion
    ADD CONSTRAINT facturacion_pkey PRIMARY KEY (id_factura);


--
-- Name: historial_medico historial_medico_cedula_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.historial_medico
    ADD CONSTRAINT historial_medico_cedula_key UNIQUE (cedula);


--
-- Name: historial_medico historial_medico_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.historial_medico
    ADD CONSTRAINT historial_medico_pkey PRIMARY KEY (id_historial);


--
-- Name: login login_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.login
    ADD CONSTRAINT login_pkey PRIMARY KEY (id_login);


--
-- Name: login login_usuario_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.login
    ADD CONSTRAINT login_usuario_key UNIQUE (usuario);


--
-- Name: pago_detalle pago_detalle_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pago_detalle
    ADD CONSTRAINT pago_detalle_pkey PRIMARY KEY (id_pago);


--
-- Name: rol rol_nombre_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rol
    ADD CONSTRAINT rol_nombre_key UNIQUE (nombre);


--
-- Name: rol rol_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rol
    ADD CONSTRAINT rol_pkey PRIMARY KEY (id_rol);


--
-- Name: sessiones sessiones_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sessiones
    ADD CONSTRAINT sessiones_pkey PRIMARY KEY (id_session);


--
-- Name: tabla_citas tabla_citas_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tabla_citas
    ADD CONSTRAINT tabla_citas_pkey PRIMARY KEY (id_citas);


--
-- Name: tabla_examenes tabla_examenes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tabla_examenes
    ADD CONSTRAINT tabla_examenes_pkey PRIMARY KEY (id_examenes);


--
-- Name: usuario usuario_correo_electronico_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT usuario_correo_electronico_key UNIQUE (correo_electronico);


--
-- Name: usuario usuario_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT usuario_pkey PRIMARY KEY (id_usuario);


--
-- Name: cita cita_id_usuario_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cita
    ADD CONSTRAINT cita_id_usuario_fkey FOREIGN KEY (id_usuario) REFERENCES public.usuario(id_usuario);


--
-- Name: tabla_examenes fk_categoria_examen; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tabla_examenes
    ADD CONSTRAINT fk_categoria_examen FOREIGN KEY (id_categoria) REFERENCES public.categoria(id_categoria);


--
-- Name: facturacion fk_examenes; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.facturacion
    ADD CONSTRAINT fk_examenes FOREIGN KEY (id_examenes) REFERENCES public.tabla_examenes(id_examenes);


--
-- Name: login fk_usuario_login; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.login
    ADD CONSTRAINT fk_usuario_login FOREIGN KEY (id_usuario) REFERENCES public.usuario(id_usuario) ON DELETE CASCADE;


--
-- Name: sessiones fk_usuario_session; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sessiones
    ADD CONSTRAINT fk_usuario_session FOREIGN KEY (id_usuario) REFERENCES public.usuario(id_usuario);


--
-- Name: login login_id_rol_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.login
    ADD CONSTRAINT login_id_rol_fkey FOREIGN KEY (id_rol) REFERENCES public.rol(id_rol);


--
-- PostgreSQL database dump complete
--

\unrestrict MkSYJtdGW4tUlHNJmspk02z1s6aqSuGxLafIRCxGLIsjmHj9gkg009M0iAvCpYt

