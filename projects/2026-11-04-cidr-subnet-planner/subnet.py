"""IPv4 CIDR planning with Python's standard library."""
import argparse
import ipaddress
import json

def describe(cidr):
    net = ipaddress.IPv4Network(cidr, strict=False)
    first = net.network_address if net.prefixlen >= 31 else net.network_address + 1
    last = net.broadcast_address if net.prefixlen >= 31 else net.broadcast_address - 1
    count = net.num_addresses if net.prefixlen >= 31 else net.num_addresses - 2
    return {"network": str(net.network_address), "prefix": net.prefixlen,
            "netmask": str(net.netmask), "broadcast": str(net.broadcast_address),
            "first_usable": str(first), "last_usable": str(last),
            "usable_hosts": count}

def split(cidr, new_prefix):
    net = ipaddress.IPv4Network(cidr, strict=False)
    if not net.prefixlen <= new_prefix <= 32:
        raise ValueError("new prefix must be between original prefix and 32")
    return [str(subnet) for subnet in net.subnets(new_prefix=new_prefix)] if new_prefix > net.prefixlen else [str(net)]

def main():
    parser = argparse.ArgumentParser(description="Plan IPv4 CIDR ranges")
    parser.add_argument("cidr")
    parser.add_argument("--split", type=int, metavar="PREFIX")
    args = parser.parse_args()
    try:
        output = describe(args.cidr)
        if args.split is not None:
            output["subnets"] = split(args.cidr, args.split)
        print(json.dumps(output, indent=2))
    except (ValueError, ipaddress.AddressValueError) as exc:
        parser.error(str(exc))

if __name__ == "__main__":
    main()
