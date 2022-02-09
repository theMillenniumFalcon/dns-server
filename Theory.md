## What is a DNS server?
- Huumans interact with inforamtion online through domain names while web browsers use IP adderesses. DNS translates domain names to IP adderesses.
- DNS servers eliminate the need for humans to memorize IP addresses.

## How does DNS work?
- The process of DNS resolution starts with converting a hostname into a computer-friendly IP address. An IP address is given to each device on the Internet, and that address is necessary to find the appropriate Internet device.

## There are 4 DNS servers involved in loading a webpage:
- DNS recursor: The recursor can be thought of as a librarian who is asked to go find a particular book somewhere in a library. The DNS recursor is a server designed to receive queries from client machines through applications such as web browsers. Typically the recursor is then responsible for making additional requests in order to satisfy the client’s DNS query.

- Root nameserver: The root server is the first step in translating (resolving) human readable host names into IP addresses. It can be thought of like an index in a library that points to different racks of books - typically it serves as a reference to other more specific locations.

- TLD nameserver: The top level domain server (TLD) can be thought of as a specific rack of books in a library. This nameserver is the next step in the search for a specific IP address, and it hosts the last portion of a hostname (In example.com, the TLD server is “com”).

- Authoritative nameserver: This final nameserver can be thought of as a dictionary on a rack of books, in which a specific name can be translated into its definition. The authoritative nameserver is the last stop in the nameserver query. If the authoritative name server has access to the requested record, it will return the IP address for the requested hostname back to the DNS Recursor (the librarian) that made the initial request.

## What's the difference between an authoritative DNS server and a recursive DNS resolver?
- The recursive DNS resolver is present at the beginning of the DNS query and the authoritative DNS server is at the end.

    ### Recursive DNS resolver:
    - The recursive resolver is the computer that responds to a recursive request from a client and takes the time to track down the DNS record. It does this by making series of requests until it reaches the authoritative DNS nameserver for the requested record (or returns an error if no record is found). But the recursive DNS resolvers do not always need to amke multiple requets in order to track down the records needed to respond to a client, caching is used to short-circuit the necessary requests by serving the requested resource record earlier in the DNS lookup.
    
    ### Authoritative DNS server:
    - A authoritative DNS server is a server that actually holds and is responsible for, DNS resource records.
    - This is the server at the bottom of the DNS lookup chain that will respond with the queried resource record, ultimately allowing the web browser making the request to reach the IP address needed to access a website or other web resources. If in the case where the query is for a subdomain such as foo.example.com, an addittional nameserver will be added to the sequence after the authoritative nameserver, which is responsible for storing the subdomain's CNAME record.
        - CNAME (canonical name) must point to a domain and not an IP address.
        - Oftentimes, when sites have subdomains such as blog.example.com or shop.example.com, those subdomains will have CNAME records that point to a root domain (example.com).
        - This way if the IP address of the host changes, only the DNS A record for the root domain needs to be updated and all the CNAME records will follow along with whatever changes are made to the root.
    
## What are the steps in a DNS lookup?
- A user types 'example.com' into a web browser and the query travels into the Internet and is received by a DNS recursive resolver.
- The resolver then queries a DNS root nameserver (.).