#!/bin/bash
# Created by (c) Henry Letellier

my_true=1
my_false=0
file_config=/etc/dhcpcd.conf

function disclaimer() {
    echo "+=====================================================+"
    echo "|        Disclaimer                                   |"
    echo "| This program is provided as                         |"
    echo "| if and without any warranty.                        |"
    echo "|                                                     |"
    echo "| If you have already configured                      |"
    echo "| a static IP for a network interface                 |"
    echo "| Please edit the file at:                            |"
    echo "| '$file_config'                                  |"
    echo "| and remove the lines:                               |"
    echo "| 'interface [INTERFACE]'                             |"
    echo "| 'static_routers=[ROUTER IP]'                        |"
    echo "| 'static domain_name_servers=[DNS IP]'               |"
    echo "| 'static ip_address=[STATIC IP ADDRESS YOU WANT]/24' |"
    echo "|                                                     |"
    echo "| Remember to save the file                           |"
    echo "| To edit the file you may need to use elevated       |"
    echo "| privileges (like sudo). You do not need to restart  |"
    echo "| the service if you are going to run this program.   |"
    echo "|                                                     |"
    echo "| This program was created by (c) Henry Letellier     |"
    echo "+=====================================================+"
}

function yes_no() {
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

function is_in_string() {
    local string="$2"
    local substring="$1"
    echo "$string" | grep -qF "$substring"
    if [ $? -eq 1 ]; then
        return $my_true
    else
        return $my_false
    fi
}

function is_only_blanks() {
    local string=$1
    local string_length=${#string}
    local string_without_blanks=${string// /}
    local string_without_blanks=${string//\t/}
    local string_without_blanks_length=${#string_without_blanks}
    if [ $string_length -eq $string_without_blanks_length ]; then
        return $my_false
    else
        return $my_true
    fi
}

function is_numeric() {
    local string=$1
    if [[ $string =~ ^[0-9]+$ ]]; then
        return $my_true
    else
        return $my_false
    fi
}

function remove_numbers() {
    local string=$1
    local string_without_numbers=${string//[0-9]/}
    echo $string_without_numbers
}

function is_ip_dots_correct_length() {
    local ip=$1
    local dots=$(remove_numbers $ip)
    local dots_length=${#dots}
    if [ $dots_length -eq 3 ]; then
        return $my_true
    else
        return $my_false
    fi
}

function is_ip() {
    local ip=$1
    local ip_length=${#ip}
    local ip_without_dots=${ip//./}
    local ip_without_dots_length=${#ip_without_dots}
    is_numeric $ip_without_dots
    local it_is_numeric=$?
    is_ip_dots_correct_length $ip
    local dots_are_correct_length=$?
    if [ $ip_without_dots_length -eq 0 ] || [ $it_is_numeric -eq $my_false ] || [ $dots_are_correct_length -eq $my_false ]; then
        return $my_false
    fi
    # if [ $ip_without_dots_length -eq 0 ]; then
    #     echo "Ip length = 0"
    #     return $my_false
    # fi
    # if [ $it_is_numeric -eq $my_false ]; then
    #     echo "Ip isn't numeric"
    #     return $my_false
    # fi
    # if [ $dots_are_correct_length -eq $my_false ]; then
    #     echo "Dots are not the right length"
    #     return $my_false
    # fi
    return $my_true
}

function is_a_network_interface() {
    local network_interface=$1
    local available_network_interfaces=$(ifconfig | grep ": " | cut -d ":" -f 1)
    is_in_string $network_interface $available_network_interfaces
    return $?
}

function replace_newlines() {
    local string=$1
    local character=$2
    local string_without_newlines=${string//$'\n'/"$character"}
    echo $string_without_newlines
}

function string_to_list() {
    local string=$1
    local character=$2
    local listed_string=$(echo "$string" | cut -d "$character" -f 1-)
    echo $listed_string
}

function remove_spaces() {
    local string=$1
    local string_without_spaces=${string// /}
    echo $string_without_spaces
}

function display_as_table() {
    local a="$(echo "${1//$'\n'/' '}" | cut -d " " -f 1-)"
    local b="$(echo "${2//$'\n'/' '}" | cut -d " " -f 1-)"
    local c="$(echo "${3//$'\n'/' '}" | cut -d " " -f 1-)"
    local e=" "
    local counter=1
    local offset_index=7
    local packet_start=$counter
    local packet_offset=$offset_index
    is_in_string " " $a
    local status_a=$?
    is_in_string " " $b
    local status_b=$?
    is_in_string " " $c
    local status_c=$?
    if [ $status_a -eq $my_false ] || [ $status_b -eq $my_false ] || [ $status_c -eq $my_false ]; then
        echo "$a - $b $c"
        return $my_true
    fi
    while [ ${#e} -ne 0 ]; do
        echo "$(echo $a | cut -d ' ' -f $counter) - $(echo $b | cut -d ' ' -f $packet_start-$packet_offset)  $(echo $c | cut -d ' ' -f $packet_start-$packet_offset)"
        let "packet_start=(counter*offset_index)+1"
        let "counter=counter+1"
        let "packet_offset=counter*offset_index"
        e=$(echo $a | cut -d ' ' -f $counter-)
    done
}

function credits() {
    echo "This program was created by (c) Henry Letellier"
}

function reboot_system() {
    yes_no "Do you wish to reboot your system?"
    if [ $? -eq $my_true ]; then
        echo "Rebooting the system"
        sudo reboot
    fi
}

function apply_configuration() {
    echo "Applying the static IP configuration"
    echo "Running: sudo echo 'interface $default_network_interface' >>$file_config"
    sudo echo "interface $default_network_interface" >>$file_config
    echo "Running: sudo echo 'static ip_address=$ip_address/24' >>$file_config"
    sudo echo "static ip_address=$ip_address/24" >>$file_config
    echo "Running: sudo echo 'static routers=$router_ip' >>$file_config"
    sudo echo "static routers=$router_ip" >>$file_config
    echo "Running: sudo echo 'static domain_name_servers=$dns_ip' >>$file_config"
    sudo echo "static domain_name_servers=$dns_ip" >>$file_config
    echo "Restarting the service"
    sudo service networking restart
    sudo systemctl restart networking
    echo "Done"
    echo "It is recommended to reboot the system when possible"
    reboot_system
    credits
}

# Gathering default information
echo "---------------------"
echo "Gathering system info"
echo "---------------------"
echo

# Get the current IP address
ifconfig_content=$(ifconfig)
echo "Getting ip address"
ip_address=$(hostname -I)
echo "IP address: $ip_address"

# Get the router's IP address
echo "Getting the routers IP address"
router_ip=$(ip r | grep "default via" | cut -d " " -f 3)
echo "Routers IP address: $router_ip"

# Get the DNS IP
echo "Getting the DNS IP address"
dns_ip=$(grep "nameserver" /etc/resolv.conf | cut -d " " -f 2)
echo "DNS IP address: $dns_ip"

# Get the netword interface
echo "Getting the active network interface"
default_network_interface=$(echo "$ifconfig_content" | grep -B1 $ip_address | cut -d ":" -f 1 | cut -d " " -f 1)
echo "Getting network interfaces"
network_interfaces=$(echo "$ifconfig_content" | grep ": " | cut -d ":" -f 1)
echo "Getting packets from networks"
packets_from_network=$(echo "$ifconfig_content" | grep "RX packets" | cut -d ":" -f 2 | cut -d " " -f 9-)
echo "Getting packets to networks"
packets_to_network=$(echo "$ifconfig_content" | grep "TX packets" | cut -d ":" -f 2 | cut -d " " -f 9-)
echo "Default network interface: $default_network_interface"
echo -e "Network interfaces:\n$network_interfaces"
echo -e "Packets from networks:\n$packets_from_network"
echo -e "Packets to networks:\n$packets_to_network"
credits

disclaimer

# Check if user wishes to set a specific IP different from the current one
echo "---------------------"
echo "Setting static IP"
echo "---------------------"
echo "DNS IP address: $dns_ip"
echo "Router IP address: $router_ip"
echo "Current IP address: $ip_address"
echo "Current network interface: $default_network_interface"
echo
echo "Do not use any ip starting by 127 because it corresponds to the localhost ip (a network internal to your system)"
echo "Avoid using ip's ending by .0 or .255 : These ip's are reserved (generally) for network management by the network administrators"
yes_no "Would you like to set a static IP address different from the listed one?"
if [ $? -eq $my_true ]; then
    echo "Please enter the static IP address you wish to set:"
    read -p "Static IP address: " static_ip_address
    is_ip $static_ip_address
    if [ $? -eq $my_true ]; then
        ip_address=$static_ip_address
        echo "The IP $static_ip_address is a correct IP, it will thus be used for the static IP"
    else
        echo "The IP you entered is incorrect, the current stored IP ($ip_address) will be used"
    fi
else
    echo "The current IP ($ip_address) will be used"
fi
credits

# Check if user wishes to set a specific router IP different from the current one
echo "---------------------"
echo "Setting DNS IP"
echo "---------------------"
echo "DNS IP address: $dns_ip"
echo "Router IP address: $router_ip"
echo "Current IP address: $ip_address"
echo "Current network interface: $default_network_interface"
echo
echo "Do not use any ip starting by 127 because it corresponds to the localhost ip (a network internal to your system)"
echo "Avoid using ip's ending by .0 or .255 : These ip's are reserved (generally) for network management by the network administrators"
yes_no "Would you like to set a DNS IP address different from the listed one?"
if [ $? -eq $my_true ]; then
    echo "Please enter the DNS IP address:"
    read -p "DNS IP address: " dns_ip_address
    is_ip $dns_ip_address
    if [ $? -eq $my_true ]; then
        dns_ip=$dns_ip_address
        echo "The DNS IP $dns_ip_address is a correct IP, it will thus be used for the DNS IP"
    else
        echo "The IP you entered is incorrect, the current stored IP ($dns_ip) will be used"
    fi
else
    echo "The current DNS IP will be used"
fi
credits

# Check if user wishes to set a specific router IP different from the current one
echo "---------------------"
echo "Setting router IP"
echo "---------------------"
echo "DNS IP address: $dns_ip"
echo "Router IP address: $router_ip"
echo "Current IP address: $ip_address"
echo "Current network interface: $default_network_interface"
echo
echo "Do not use any ip starting by 127 because it corresponds to the localhost ip (a network internal to your system)"
echo "Avoid using ip's ending by .0 or .255 : These ip's are reserved (generally) for network management by the network administrators"
yes_no "Would you like to set a router IP address different from the listed one?"
if [ $? -eq $my_true ]; then
    echo "Please enter the router IP address:"
    read -p "Router IP address: " router_ip_address
    is_ip $router_ip_address
    if [ $? -eq $my_true ]; then
        router_ip=$router_ip_address
        echo "The router IP $router_ip_address is a correct IP, it will thus be used for the router IP"
    else
        echo "The IP you entered is incorrect, the current stored IP ($router_ip) will be used"
    fi
else
    echo "The current router IP will be used"
fi
credits

# Set the interface
echo "---------------------"
echo "Setting interface"
echo "---------------------"
echo "DNS IP address: $dns_ip"
echo "Router IP address: $router_ip"
echo "Current IP address: $ip_address"
echo "Current network interface: $default_network_interface"
echo
echo "Here are the available network interfaces and their trafic flow"
echo "wlan: wifi, eth: ethernet, lo: local"
echo "Please note the 'lo' means 'local' (it is an 'intranet' to the system, for example it is used docker containers)"
echo "The second name of 'lo' is 'localhost' that you might have used when testing locally deployed websites"
echo
display_as_table "$network_interfaces" "$packets_from_network" "$packets_to_network"
echo
yes_no "Would you like to set a network interface different from the listed one?"
if [ $? -eq $my_true ]; then
    echo "Please enter the network interface:"
    read -p "Network interface address: " network_interface
    is_a_network_interface $network_interface
    if [ $? -eq $my_true ]; then
        default_network_interface=$network_interface
        echo "The Network interface $network_interface is a correct IP, it will thus be used for the network interface"
    else
        echo "The network interface you entered is incorrect, the current stored IP ($default_network_interface) will be used"
    fi
else
    echo "The current Network interface will be used"
fi
credits

# removing spaces from the stored variables
ip_address=$(remove_spaces $ip_address)
router_ip=$(remove_spaces $router_ip)
dns_ip=$(remove_spaces $dns_ip)

apply_configuration
