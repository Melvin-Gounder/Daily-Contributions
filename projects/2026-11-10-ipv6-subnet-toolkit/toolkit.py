"""IPv6 planning helpers using the Python standard library."""
import argparse
import ipaddress

def parse_network(value):
    if "/" not in value:
        raise ValueError("CIDR prefix required")
    try:
        return ipaddress.IPv6Network(value, strict=True)
    except (ipaddress.AddressValueError, ipaddress.NetmaskValueError) as exc:
        raise ValueError(str(exc)) from exc

def summarize(cidr):
    network = parse_network(cidr)
    return {
        "network": str(network),
        "prefix": network.prefixlen,
        "addresses": network.num_addresses,
        "first": str(network.network_address),
        "last": str(network.broadcast_address),
    }

def contains(cidr, address):
    network = parse_network(cidr)
    try:
        ip = ipaddress.ip_address(address)
    except ValueError as exc:
        raise ValueError("invalid IP address") from exc
    return isinstance(ip, ipaddress.IPv6Address) and ip in network

def partition(cidr, new_prefix, limit=256):
    network = parse_network(cidr)
    if not network.prefixlen <= new_prefix <= 128:
        raise ValueError("new prefix must be between current prefix and 128")
    if limit < 1:
        raise ValueError("limit must be positive")
    count = 1 << (new_prefix - network.prefixlen)
    if count > limit:
        raise ValueError(f"{count} subnets exceed limit {limit}")
    return [str(net) for net in network.subnets(new_prefix=new_prefix)] if new_prefix > network.prefixlen else [str(network)]

def address_at(cidr, offset):
    network = parse_network(cidr)
    if not isinstance(offset, int) or isinstance(offset, bool) or not 0 <= offset < network.num_addresses:
        raise ValueError("offset outside network")
    return str(network.network_address + offset)

def main():
    parser = argparse.ArgumentParser(description="Strict IPv6 subnet planning")
    parser.add_argument("cidr", help="Canonical IPv6 network CIDR")
    parser.add_argument("--split", type=int, help="New prefix length")
    parser.add_argument("--limit", type=int, default=256)
    args = parser.parse_args()
    if args.split is None:
        for key, value in summarize(args.cidr).items():
            print(f"{key}: {value}")
    else:
        for net in partition(args.cidr, args.split, args.limit):
            print(net)

if __name__ == "__main__":
    main()
