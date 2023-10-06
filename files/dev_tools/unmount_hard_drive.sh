#!/bin/bash
hl_true=1
hl_false=0
colour_a='\033[1;32m'
colour_c='\033[1;31m'
colour_e='\033[1;33m'
colour_r='\033[0m'

function cecho() {
    cecho -e "$colour_a$1$colour_r"
}

function yn_question() {
    while true; do
        read -p "$colour_a$1 [(y)es/(N)o]$colour_r" yn
        case $yn in
        [Yy]*)
            return $hl_true
            break
            ;;
        [Nn]*)
            return $hl_false
            break
            ;;
        *)
            echo -e "${colour_c}Please answer y for yes or n for no.$colour_r"
            ;;
        esac
    done
}

function ask_for_hard_drive() {
    read -p "${colour_a}External hard drive name: $colour_r" external_drive_name
    echo "$external_drive_name"
}

function get_hard_drive_name() {
    cecho "Displaying available hard drives: (with lsblk -f)"
    sudo lsblk -f
    cecho "Please enter the name of the external hard drive:"
    cecho "Ex: sda1"
}

function is_drive_mounted() {
    local drive_name=$1
    local drive_mounted=$hl_false
    local drive_mounted=$(df -h | grep $drive_name | wc -l)
    if [ $drive_mounted -eq 0 ]; then
        return $hl_false
    else
        return $hl_true
    fi
}

function is_only_blanks() {
    local string=$1
    local string_length=${#string}
    local string_without_blanks=${string// /}
    local string_without_blanks_length=${#string_without_blanks}
    if [ $string_length -eq $string_without_blanks_length ]; then
        return $hl_false
    else
        return $hl_true
    fi
}

function is_first_character_a_number() {
    local string=$1
    local first_character=${string:0:1}
    if [[ $first_character =~ ^[0-9]+$ ]]; then
        return $hl_true
    else
        return $hl_false
    fi
}

function drive_has_illegal_characters() {
    local string=$1
    local string_length=${#string}
    local string_without_illegal_characters=${string//[^a-zA-Z0-9_-]/}
    local string_without_illegal_characters_length=${#string_without_illegal_characters}
    if [ $string_length -eq $string_without_illegal_characters_length ]; then
        return $hl_false
    else
        return $hl_true
    fi
}

function get_mount_name() {
    local mount_name=""
    local blanks_status=$hl_false
    local illegal_characters_status=$hl_false
    local stop_loop=$hl_false
    while [ ${#mount_name} -eq 0 ] && [ $stop_loop -eq $hl_false ]; do
        cecho "Please enter the name you wish to assign to the drive when mounted:" >&2
        read -p "${colour_a}Mount name: $colour_r" mount_name
        cecho "mount_name = $colour_e$mount_name" >&2
        is_only_blanks "$mount_name"
        blanks_status=$?
        if [ $blanks_status -eq $hl_true ]; then
            echo "Please enter an alphanumeric name (- and _ are also allowed)" >&2
            mount_name=""
        fi
        drive_has_illegal_characters "$mount_name"
        illegal_characters_status=$?
        if [ $illegal_characters_status -eq $hl_true ]; then
            echo "Please enter an alphanumeric name (only letters and numbers) + - and _ characters" >&2
            mount_name=""
        fi
        if [ $blanks_status -eq $hl_false ] && [ $illegal_characters_status -eq $hl_false ]; then
            stop_loop=$hl_true
            break
        fi
    done
    is_first_character_a_number $mount_name
    if [ $? -eq $hl_true ]; then
        mount_name="drive$mount_name"
        echo "The first character was a number, thus, the new name is: $mount_name" >&2
    fi
    echo "$mount_name"
}

function mount_drive() {
    local drive=$1
    local drive_name=""
    local mount_drive=$hl_false
    yn_question "Do you wish to mount $drive?"
    mount_drive=$?
    if [ $mount_drive -eq $hl_true ]; then
        drive_name=$(get_mount_name)
        sudo mkdir -p /media/$USER/$drive_name
        sudo mount /dev/$drive /media/$USER/$drive_name
    fi
}

function unmount_drive() {
    local drive=$1
    local drive_name=""
    local unmount_drive=$hl_false
    yn_question "Do you wish to unmount $drive?"
    unmount_drive=$?
    if [ $unmount_drive -eq $hl_true ]; then
        drive_name=$(get_mount_name)
        sudo umount /dev/$drive
    fi
}

function main() {
    local drive_name=""
    local drive_mounted=$hl_false

    get_hard_drive_name
    drive_name=$(ask_for_hard_drive)
    is_drive_mounted $drive_name
    drive_mounted=$?
    if [ $drive_mounted -eq $hl_true ]; then
        echo "Drive $drive_name is mounted"
        unmount_drive $drive_name
        is_drive_mounted $drive_name
        drive_mounted=$?
        if [ $drive_mounted -eq $hl_true ]; then
            echo "Drive $drive_name is mounted"
        else
            echo "Drive $drive_name is not mounted"
        fi
    else
        echo "Drive $drive_name is not mounted"
        mount_drive $drive_name
        is_drive_mounted $drive_name
        drive_mounted=$?
        if [ $drive_mounted -eq $hl_true ]; then
            echo "Drive $drive_name is mounted"
        else
            echo "Drive $drive_name is not mounted"
        fi
    fi
}

main
