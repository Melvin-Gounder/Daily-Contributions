# IPv4 CIDR Subnet Planner

Use `python subnet.py 192.168.10.44/24` to calculate the containing network, mask, broadcast, usable range, and host count. Use `python subnet.py 10.0.0.0/24 --split 26` to enumerate four /26 networks. Run tests with `python -m unittest -v test_subnet.py`.

A /24 contains 256 addresses, with 254 conventional usable hosts. A /31 is a point-to-point range with both addresses usable (RFC 3021); /32 identifies one address. `strict=False` deliberately normalizes a host/prefix into its containing network. The subnet listing is exhaustive and can be large for very broad networks. Python 3.9+; no external packages.
