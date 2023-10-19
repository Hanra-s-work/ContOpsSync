#!/bin/bash

function run_command() {
 echo "Running! $@"
 $@
}

run_command echo "hi"
run_command echo "hello world"
