--
-- PostgreSQL database dump
--

-- Dumped from database version 16.1
-- Dumped by pg_dump version 16.1

-- PostgreSQL oturum ayarlarını yapın
SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

REVOKE ALL PRIVILEGES ON SCHEMA public FROM biadago;
REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA public FROM biadago;
REVOKE ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public FROM biadago;

-- Django'nun PostgreSQL veritabanında gerekli izinleri sağlayın
GRANT ALL PRIVILEGES ON SCHEMA public TO biadago;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO biadago;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO biadago;

--
-- PostgreSQL database dump complete
--

