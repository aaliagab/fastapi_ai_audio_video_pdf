-- phpMyAdmin SQL Dump
-- version 3.4.9
-- http://www.phpmyadmin.net
--
-- Servidor: localhost
-- Tiempo de generación: 27-05-2024 a las 21:10:53
-- Versión del servidor: 5.5.20
-- Versión de PHP: 5.3.9

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Base de datos: `aicontext`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `access`
--

CREATE TABLE IF NOT EXISTS `access` (
  `accesstoken_id` char(36) COLLATE latin1_spanish_ci NOT NULL COMMENT '(DC2Type:uuid)',
  `access_name` varchar(255) COLLATE latin1_spanish_ci NOT NULL,
  PRIMARY KEY (`accesstoken_id`),
  UNIQUE KEY `access_name` (`access_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;

--
-- Volcado de datos para la tabla `access`
--

INSERT INTO `access` (`accesstoken_id`, `access_name`) VALUES
('c832fa51-bc2c-4ba8-9266-7c8f92a3f9c7', 'admin'),
('e82251a3-9f1b-481a-bbb1-79cc2bc83d53', 'editor');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `content`
--

CREATE TABLE IF NOT EXISTS `content` (
  `id` char(36) COLLATE latin1_spanish_ci NOT NULL COMMENT '(DC2Type:uuid)',
  `source_id` char(36) COLLATE latin1_spanish_ci NOT NULL,
  `access_id` char(36) COLLATE latin1_spanish_ci NOT NULL,
  `title` varchar(255) COLLATE latin1_spanish_ci NOT NULL,
  `phrase` text COLLATE latin1_spanish_ci NOT NULL,
  `date_add` datetime DEFAULT NULL,
  `date_upd` datetime DEFAULT NULL,
  `status` tinyint(4) DEFAULT NULL COMMENT '1=activo, 0=inactivo',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `source_id` (`source_id`),
  KEY `access_id` (`access_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;

--
-- Volcado de datos para la tabla `content`
--

INSERT INTO `content` (`id`, `source_id`, `access_id`, `title`, `phrase`, `date_add`, `date_upd`, `status`) VALUES
('1fc60c8e-b6c0-4b91-a0ad-82e135a4bb5c', 'caf858bb-97fe-48f2-b362-49a89c195eb6', 'c832fa51-bc2c-4ba8-9266-7c8f92a3f9c7', 'Grabación.wav', ' Consiste en poder subir clic de videos y audio, transcribirnos. Esto mejor hacerlo con otras herramientas tipo Google ya que con OpenAI se encarece. Enviar el texto escrito para poder hacer nuevo con sus intastipos y trajes de texto, pero solo de los textos transcritos. No de otro tipo de contenido no precarregado.', '2024-05-27 14:53:45', '2024-05-27 14:53:45', 1),
('87885719-8701-4dd8-b803-cab7b5f88a4b', 'caf858bb-97fe-48f2-b362-49a89c195eb6', 'e82251a3-9f1b-481a-bbb1-79cc2bc83d53', 'Documentacion para el proyecto.pdf', 'Buenas tardes, Adriel.  \n \nSegún comentaba durante nuestra llamada de ayer, la intención es clasificar todo el contenido que podemos \nsubir en audio, video o pdf según su fuente, para lo que deberíamos mandar un campo "source_token" en \nel endpoint de subida de contenido con esta fina lidad.  \nPor otro lado, al consultar, debemos mandar otro parámetro "access_token" que identificará quienes pueden \nconsultar qué contenido.  \n \nYo haré un front que consulte tu API y otros servicios. Desde la subida del contenido con el usuario (source) \nidentificado, hasta el login de usuarios que puedan ver determinado tipo de contenido.  Respecto al modelo \nde datos, yo me imagino algo así.  \n \nTable User { \n  id char(36) [pk, unique, note:"(DC2Type:uuid)" ] \n  user_name varchar \n  user_email varchar \n  user_phone varchar \n  user_password varchar \n  date_add datetime  \n  date_upd datetime  \n} \n \nTable Source {  \n  id char(36) [pk, unique, note:"(DC2Type:uuid)" ] \n  source_name varchar \n  user_id char(36) [ref: > User.id]  \n  date_add datetime  \n  date_upd datetime  \n} \n \nTable Content{  \n  id char(36) [pk, unique, note:"(DC2Type:uuid)" ] \n  source_id char(36) [ref: > Source .id] \n  access_id char(36) [ref: > Access .accesstoken_id]  \n  title varchar \n  phrase varchar(max) \n  date_add datetime  \n  date_upd datetime  \n  status tinyint [note:"1=activo, 0=inactivo" ] \n} \n \n \nTable Access{ \n  accesstoken_id char(36) [note:"(DC2Type:uuid)" ]   \n} \n \nTable UserAccess{  \n  user_id char(36) [ref: > User.id]  \n  accesstoken_id char(36) [ref: > Access .accesstoken_id]  \n} \n \nTabla User  dónde iremos almacenando los usuarios.  \nTabla Source dónde guardaremos a quienes serán generadores de contenido, que a la vez pueden estar \nrelacionados con un perfil de usuario.  Tabla Content dónde, de alguna forma, deberemos referenciar al contenido guardado para GPT, y que irá \nrelacionado con un source_id.  \nTabla Access que contendrá un accestoken  que podrá estar relacionado con uno o más content_id . Como \npara crear un grupo de acceso. Todo el que tenga ese accesstoken podrá acceder a todo el contenido \nrelacionado.  \nY por último la tabla que relaciona al usuario con el accestoken.  \n \nTe dejo el diagrama aquí  \nhttps://dbdiagram.io/d/GA -663f8aec9e85a46d55941b55  \n \nPor favor, estímame  cuanto  puede ser en coste y tiempo adaptar la API para para que la carga de contenido \npueda aceptar un parámetro   "source_token" y que la respuesta de contenido en su llamada acepte un \naccestoken  para que solo devuelva el contenido refe renciado a ese token.  \n \nCualquier duda comentamos.  \nGracias  \n \n///////////////////////////////////////////////////////////  \n \nTabla User  dónde iremos almacenando los usuarios.  \nTabla Source dónde guardaremos a quienes serán generadores de contenido, que a la vez pueden estar relacionados \ncon un perfil de usuario.  \nTabla Content dónde, de alguna forma, deberemos referenciar al contenido guard ado para GPT, y que irá relacionado \ncon un source_id.  \nTabla Access que contendrá un accestoken que podrá estar relacionado con uno o más content_id. Como para crear \nun grupo de acceso. Todo el que tenga ese accesstoken podrá acceder a todo el contenido rel acionado.  \nY por último la tabla que relaciona al usuario con el accestoken.  \nDebemos garantizar entonces que los usuarios al loguearse si tiene relacion con algun source entonces este usuario \nes generador de contenido por tanto tiene acceso a subir contenid o y a leer o chatear con cualquier contenido \ngenerado con su source, asi como leer o chatear con cualquier contenido que pertenezca a sus accesos. Esto significa \nque cada contenido tiene referencia de un source pero tambien tiene referencia del acceso, ent onces cuando un \nusuario suba su contenido debe decidir cual de sus acceso conceder a este contenido.  \n \nLos pasos a seguir serían los siguientes:  \n1. Implementar  la lógica  de autenticación  de usuarios : \no Crear un endpoint  para autenticar usuarios y obtener su información, incluyendo los "sources" y \ngrupos de acceso asociados.  \n2. Implementar  la lógica  para  crear  y administrar  "sources" : \no Crear endpoints para crear, leer, actualizar y eliminar "sources".  \no En versiones posteriores al MVP asegurarse de que solo los usuarios autorizados puedan administrar \nsus propios "sources".  \n3. Implementar  la lógica  para  crear  y administrar  contenido : \no Crear endpoints para crear, leer, actualizar y eliminar contenido.  \no Al crear un nuevo contenido, el usuario deberá proporcionar el "source_id" y el "access_id" \ncorrespondiente.  \no En versiones posteriores al MVP asegurarse de que solo los usuarios autorizados puedan crear y \nadministrar contenido relacionado con sus "sources" y grupos de acceso.  \n4. Implementar  la lógica  para  administrar  grupos  de acceso : \no Crear endpoints para crear, leer, actualizar y eliminar grupos de acceso.  \no Asegurarse de que solo los usuarios autorizados puedan administrar los grupos de acceso.  \n5. Implementar  la lógica  para  asociar  usuarios  con grupos  de acceso : \no Crear endpoints  para asociar y desasociar usuarios con grupos de acceso.  \no Asegurarse de que solo los usuarios autorizados puedan realizar estas operaciones.  \n6. Implementar  la lógica  de control  de acceso : \no Crear middlewares o dependencias para verificar los permisos de acceso en cada endpoint protegido.  o Asegurarse de que solo los usuarios autorizados puedan acceder al contenido según sus "sources" y \ngrupos de acceso.  \n7. Integrar  con GPT: \no Implementar la lógica para almacenar y recuperar el contenido relacionado con GPT.  \no Asegurarse de que solo el contenido autorizado sea accesible para GPT.  \n8. Pruebas  y documentación : \no Crear pruebas unitarias y de integración para verificar el correcto funcionamiento de todas las \nfuncionalidades.  \no Documentar la API y proporcionar ejemplos de uso.  \n \n \n \n \n \n \n \n \n \n ', '2024-05-27 14:51:24', '2024-05-27 14:51:24', 1),
('a60c9bcf-adb3-413e-bd30-64e6a3c90dd5', 'caf858bb-97fe-48f2-b362-49a89c195eb6', 'c832fa51-bc2c-4ba8-9266-7c8f92a3f9c7', 'Ejemplo de Entrevista de trabajo en INGLÉS.mp4', ' Okay, welcome nice to meet you. My name is John. I''m going to be interviewing you. Okay, so why don''t we start with your name? Yes, thank you. My name is Alejandro. Carlos Alejandro. Okay, and your last name is? My last name is Nopeda. Very good. Where do you live? I live in Medellin. I have a house near to San Diego. Nice. And what is your nationality? I was born in Colombia. I am a Colombian. Interesting. Could you tell me about your family? Okay, I am married. I live with my beautiful wife. Her name is Anna. And we both have a fantastic daughter. Her name is Samantha. We love having dinner together, going to the movies. And I just love my family. I want to spend as much time as I can with them. Do you have any hobbies? As I mentioned before, I love reading. But I also love exercising. I play soccer, volleyball, and sometimes I go jogging. I don''t watch a lot of television, but I do love watching movies. Alright, let me ask you something. Why do you want to work here? I have always admired this company, and it will be a dream coming true working here. I have seen a lot of your projects, and I feel very, very connected with them. That''s why I would like to have a chance here working with you guys. Okay, in case this time you don''t get the job, would you be interested in another process with us? Absolutely. If this is not my time, so be it. But I really would like to have more chances to have these interviews and making sure that you really know what I am capable of, and that you know my desires of working here. Okay, that will be all. Thank you very much for coming. No thank you for your time.', '2024-05-27 14:58:46', '2024-05-27 14:58:46', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `source`
--

CREATE TABLE IF NOT EXISTS `source` (
  `id` char(36) COLLATE latin1_spanish_ci NOT NULL COMMENT '(DC2Type:uuid)',
  `source_name` varchar(255) COLLATE latin1_spanish_ci NOT NULL,
  `user_id` char(36) COLLATE latin1_spanish_ci NOT NULL,
  `date_add` datetime DEFAULT NULL,
  `date_upd` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;

--
-- Volcado de datos para la tabla `source`
--

INSERT INTO `source` (`id`, `source_name`, `user_id`, `date_add`, `date_upd`) VALUES
('caf858bb-97fe-48f2-b362-49a89c195eb6', 'source_admin', 'b1f5a5dc-fbda-4319-80e5-ab890b0b922c', '2024-05-26 18:56:50', '2024-05-26 18:56:50');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `user`
--

CREATE TABLE IF NOT EXISTS `user` (
  `id` char(36) COLLATE latin1_spanish_ci NOT NULL COMMENT '(DC2Type:uuid)',
  `user_name` varchar(255) COLLATE latin1_spanish_ci NOT NULL,
  `user_email` varchar(255) COLLATE latin1_spanish_ci DEFAULT NULL,
  `user_phone` varchar(255) COLLATE latin1_spanish_ci DEFAULT NULL,
  `user_password` varchar(255) COLLATE latin1_spanish_ci NOT NULL,
  `date_add` datetime DEFAULT NULL,
  `date_upd` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_name` (`user_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;

--
-- Volcado de datos para la tabla `user`
--

INSERT INTO `user` (`id`, `user_name`, `user_email`, `user_phone`, `user_password`, `date_add`, `date_upd`) VALUES
('4357296b-1e55-4ab8-a3dc-0a78c80efa05', 'adriel', 'adriel@a.aa', '95959595', '91e21671be6d7a68a84e7eaffc23a54d', '2024-05-25 15:40:14', '2024-05-25 16:56:34'),
('b1f5a5dc-fbda-4319-80e5-ab890b0b922c', 'admin', 'admin@a.aa', '', 'f6fdffe48c908deb0f4c3bd36c032e72', '2024-05-24 03:21:55', '2024-05-24 03:21:55');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `useraccess`
--

CREATE TABLE IF NOT EXISTS `useraccess` (
  `user_id` char(36) COLLATE latin1_spanish_ci NOT NULL DEFAULT '',
  `accesstoken_id` char(36) COLLATE latin1_spanish_ci NOT NULL DEFAULT '',
  PRIMARY KEY (`user_id`,`accesstoken_id`),
  KEY `accesstoken_id` (`accesstoken_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;

--
-- Volcado de datos para la tabla `useraccess`
--

INSERT INTO `useraccess` (`user_id`, `accesstoken_id`) VALUES
('b1f5a5dc-fbda-4319-80e5-ab890b0b922c', 'c832fa51-bc2c-4ba8-9266-7c8f92a3f9c7'),
('4357296b-1e55-4ab8-a3dc-0a78c80efa05', 'e82251a3-9f1b-481a-bbb1-79cc2bc83d53');

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `content`
--
ALTER TABLE `content`
  ADD CONSTRAINT `content_ibfk_1` FOREIGN KEY (`source_id`) REFERENCES `source` (`id`),
  ADD CONSTRAINT `content_ibfk_2` FOREIGN KEY (`access_id`) REFERENCES `access` (`accesstoken_id`);

--
-- Filtros para la tabla `source`
--
ALTER TABLE `source`
  ADD CONSTRAINT `source_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

--
-- Filtros para la tabla `useraccess`
--
ALTER TABLE `useraccess`
  ADD CONSTRAINT `useraccess_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  ADD CONSTRAINT `useraccess_ibfk_2` FOREIGN KEY (`accesstoken_id`) REFERENCES `access` (`accesstoken_id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
