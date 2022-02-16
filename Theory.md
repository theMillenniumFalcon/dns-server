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
- The root server then responds to the resolver with the adderess of a Top Level Domain (TLD) DNS server (such as .com or .net), which the information for its domains. When searching for example.com, our request is pointed toward the .com TLD.
- The resolver then makes a request to the .com TLD.
- The TLD server then responds with the IP adderess of the domain's nameserver, example.com
- Lastly, the recursive  resolver sends a quwery to the domain's nameserver.
- The IP address for example.com is then returned to the resolver from the nameserver.
- The DNS resolver then responds to the web browser with the IP address of the domain requested initially.
<br><hr>
Once the 8 steps of the DNS lookup have returned the IP address for example.com, the browser is able to make the request for the web page:
- The Browser makes the HTTP request to the IP address.
- The server at the IP returns the webpage to the rendered in the browser.

## What is a DNS resolver?
- The Dns reolver is the forst step in the process of DNS lookup, and it is responsible for dealing with the client that made the initial request. The resolver initiates the queries that ultimately leads to the translation of the URL to th eappropriate IP address.
```
A typical uncached DNS lookup will involve both recursive and iterative queries.
```
There is a difference between a recursive DNS resolver and a recursive query. The query refers the request made to the DNS resolver requiring the resolution of the query. A DNS recursive resolver is the computer that accepts a recursive query and processes the response by making the necessary requests.

## What are the different types of DNS queries?
- In a typical DNS lookup threee types of queries occur. By using a combination of these queries, an optimal process for DNS resolution can result in a erduction of distance traveled. In an ideal situation cached record data will be available, allowing a DNS name server to return a non-recursive query.
### 3 types of DNS queries:
- Recursive query: In a recursive query, a DNS client requires that a DNS server (typically a DNS recursive resolver) will responds to a clinet with respond to the client with either the requested resource record or an error message if the resolver can't find the record.
- Iterative query: In this situation the DNS client will allow a DNS server to return the best answer it can. If the queried DNS server does not have a match for the query name, it will return a referral to a DNS server authoritative for a lower level of the domain namespace. The DNS client will then make a query to the referral address.
- Non-recursive query: Typically this will occur when a DNS resolver client queries a DNS server for record that it has access to either because it's authoritative for the record or the record exists inside of its cache. Typically, a DNS server will cache DNS records to prevent additional consumption and load on upstream servers.

## DNS caching and where it occurs?
- The purpose of caching is to temporarily stored data in a location that results in improvements in performance and reliability for data requests. DNS caching involves storing data closer to the requesting client so that the DNS query can be resolved earlier and additional queries further down the DNS lookup chain can be avoided, thereby improving load times and reducing bandwidth/CPU consumption. The DNS data can be cached in a variety of locations, each of which will store DNS records for a set amount of time determined by the time-to-live(TTL).

## Browser DNS caching:
- Modern web browsers are designed to store cached data for a set amount of time for obvious reasons. The closer the DNS caching occurs to the web browser, the fewer processing steps must be taken in order to check the cache and make the correct requests to an IP address. Browser cache is the first cache that is checked when a request is made.

## Operating System level DNS caching:
- The Operating System level DNS caching is the second and last stop before a DNS query leaves the machine. The process inside your operating system that is designed to handle this query is commonly called a “stub resolver” or DNS client. When a stub resolver gets a request from an application, it first checks its own cache to see if it has the record. If it does not, it then sends a DNS query (with a recursive flag set), outside the local network to a DNS recursive resolver inside the Internet service Provider (ISP).
- When the recursive resolver inside the ISP recieves a DNS query, like all previous steps, it will also check to see if the requested host-to-IP adderess translation is already stored inside its persistence layer.