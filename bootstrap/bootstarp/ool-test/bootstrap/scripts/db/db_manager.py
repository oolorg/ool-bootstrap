#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import os
import log

_db_path=os.path.abspath(os.path.dirname(__file__)) + "/../../db/bootstrap.db"

def execute(sql):
	log.debug(sql)
	con=sqlite3.connect(_db_path)
	cur=con.cursor()
	cur.execute(sql)
	try:
        	con.commit()
	finally:	
		cur.close()
		con.close()

def select(sql):
	log.debug(sql)
        con=sqlite3.connect(_db_path)
	try:
		cur=con.execute(sql)
		ret=cur.fetchall()
		log.debug(ret)
	finally:
		cur.close()
		con.close()
	return ret

def connect():
	return sqlite3.connect(_db_path)

def initialize():
	con=sqlite3.connect(_db_path)
	cur = con.cursor()

	cur.execute("""create table if not exists scenarios (
	             uuid text primary key not null,
	             scenario text not null,
		     status integer default 0)""")

	cur.execute("""create table if not exists stacks (
	             id integer primary key autoincrement not null,
	             stack_id text not null,
	             scid text not null,
	             deleted bool default 0,
	             host text,
	             ip text,
	             netns text,
	             manager bool default 0)""")

	cur.execute("""create table if not exists lb_scenario (
	             pool_id text primary key not null,
	             method text,
	             protocol text,
	             subnet_id text, 
	             scid text not null)""")

	cur.execute("""create table if not exists lb_vip (
	             uuid text primary key not null,
	             vip text not null,
	             pool_id text not null)""")

	cur.execute("""create table if not exists lb_member (
	             uuid text primary key not null,
	             ip text,
	             port text,
	             pool_id text not null)""")

	con.commit()
	cur.close()
	con.close()
