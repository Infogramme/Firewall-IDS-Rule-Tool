import argparse
import json
from datetime import datetime

IPTABLES_TEMPLATE = "iptables -A {chain} -s {src_ip} -d {dst_ip} -p {protocol} --dport {port} -j {action}"
SNORT_TEMPLATE = "alert {protocol} {src_ip} any -> {dst_ip} {port} (msg:\"{message}\"; sid:{sid}; rev:1;)"


def generate_iptables_rule(config):
    return IPTABLES_TEMPLATE.format(
        chain=config.get("chain", "INPUT"),
        src_ip=config.get("src_ip", "0.0.0.0/0"),
        dst_ip=config.get("dst_ip", "0.0.0.0/0"),
        protocol=config.get("protocol", "tcp"),
        port=config.get("port", "80"),
        action=config.get("action", "ACCEPT")
    )


def generate_snort_rule(config):
    return SNORT_TEMPLATE.format(
        protocol=config.get("protocol", "tcp"),
        src_ip=config.get("src_ip", "any"),
        dst_ip=config.get("dst_ip", "any"),
        port=config.get("port", "80"),
        message=config.get("message", "Suspicious traffic detected"),
        sid=config.get("sid", int(datetime.now().timestamp()))
    )


def load_config(config_file):
    with open(config_file, 'r') as file:
        return json.load(file)


def main():
    parser = argparse.ArgumentParser(description="Firewall/IDS Rule Generator")
    parser.add_argument("--config", required=True, help="Path to the JSON config file")
    parser.add_argument("--type", choices=["iptables", "snort"], required=True, help="Type of rule to generate")
    args = parser.parse_args()

    config = load_config(args.config)

    if args.type == "iptables":
        rule = generate_iptables_rule(config)
    else:
        rule = generate_snort_rule(config)

    print("Generated Rule:\n" + rule)


if __name__ == "__main__":
    main()