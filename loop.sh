#!/usr/bin/env bash
while :;do
	./online_notif.py
	sleep $(($RANDOM % 5 + 1))m
done
