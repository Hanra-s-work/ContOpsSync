#!/bin/bash
my_true=1
my_false=0

function yn_question() {
    while true; do
        read -p "$1 [(y)es/(N)o]" yn
        case $yn in
        [Yy]*)
            return $my_true
            break
            ;;
        [Nn]*)
            return $my_false
            break
            ;;
        *)
            echo "Please answer y for yes or n for no."
            ;;
        esac
    done
}

function ask_for_hard_drive() {
    read -p "External hard drive name: " external_drive_name
    echo "$external_drive_name"
}

function get_hard_drive_name() {
    echo "Displaying available hard drives: (with lsblk -f)"
    sudo lsblk -f
    echo "Please enter the name of the external hard drive:"
    echo "Ex: sda1"
}

function is_drive_mounted() {
    local drive_name=$1
    local drive_mounted=$my_false
    local drive_mounted=$(df -h | grep $drive_name | wc -l)
    if [ $drive_mounted -eq 0 ]; then
        return $my_false
    else
        return $my_true
    fi
}

function is_only_blanks() {
    local string=$1
    local string_length=${#string}
    local string_without_blanks=${string// /}
    local string_without_blanks_length=${#string_without_blanks}
    if [ $string_length -eq $string_without_blanks_length ]; then
        return $my_false
    else
        return $my_true
    fi
}

function is_first_character_a_number() {
    local string=$1
    local first_character=${string:0:1}
    if [[ $first_character =~ ^[0-9]+$ ]]; then
        return $my_true
    else
        return $my_false
    fi
}

function drive_has_illegal_characters() {
    local string=$1
    local string_length=${#string}
    local string_without_illegal_characters=${string//[^a-zA-Z0-9_-]/}
    local string_without_illegal_characters_length=${#string_without_illegal_characters}
    if [ $string_length -eq $string_without_illegal_characters_length ]; then
        return $my_false
    else
        return $my_true
    fi
}

function get_mount_name() {
    local mount_name=""
    local blanks_status=$my_false
    local illegal_characters_status=$my_false
    local stop_loop=$my_false
    while [ ${#mount_name} -eq 0 ] && [ $stop_loop -eq $my_false ]; do
        echo "Please enter the name you wish to assign to the drive when mounted:" >&2
        read -p "Mount name: " mount_name
        echo "mount_name = $mount_name" >&2
        is_only_blanks "$mount_name"
        blanks_status=$?
        if [ $blanks_status -eq $my_true ]; then
            echo "Please enter an alphanumeric name (- and _ are also allowed)" >&2
            mount_name=""
        fi
        drive_has_illegal_characters "$mount_name"
        illegal_characters_status=$?
        if [ $illegal_characters_status -eq $my_true ]; then
            echo "Please enter an alphanumeric name (only letters and numbers) + - and _ characters" >&2
            mount_name=""
        fi
        if [ $blanks_status -eq $my_false ] && [ $illegal_characters_status -eq $my_false ]; then
            stop_loop=$my_true
            break
        fi
    done
    is_first_character_a_number $mount_name
    if [ $? -eq $my_true ]; then
        mount_name="drive$mount_name"
        echo "The first character was a number, thus, the new name is: $mount_name" >&2
    fi
    echo "$mount_name"
}

function mount_drive() {
    local drive=$1
    local drive_name=""
    local mount_drive=$my_false
    yn_question "Do you wish to mount $drive?"
    mount_drive=$?
    if [ $mount_drive -eq $my_true ]; then
        drive_name=$(get_mount_name)
        sudo mkdir -p /media/$USER/$drive_name
        sudo mount /dev/$drive /media/$USER/$drive_name
    fi
}

function main() {
    local drive_name=""
    local drive_mounted=$my_false

    get_hard_drive_name
    drive_name=$(ask_for_hard_drive)
    is_drive_mounted $drive_name
    drive_mounted=$?
    if [ $drive_mounted -eq $my_true ]; then
        echo "Drive $drive_name is mounted"
    else
        echo "Drive $drive_name is not mounted"
        mount_drive $drive_name
        is_drive_mounted $drive_name
        drive_mounted=$?
        if [ $drive_mounted -eq $my_true ]; then
            echo "Drive $drive_name is mounted"
        else
            echo "Drive $drive_name is not mounted"
        fi
    fi
}

main
