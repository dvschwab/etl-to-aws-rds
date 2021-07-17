# An Amazon RDS MySQL Instance: Design and Implementation

Amazon's Relational Database Service (RDS) is a straightforward, yet powerful way to gently transition smaller database projects to the cloud. Once the RDS service is provisioned and access established, database implementation and ETL can proceed along standard lines. The advantage of using Amazon's cloud is that they handle the administration tasks that typically require a full-time db admin: maintaining the database file system, provisioning backups, and applying software updates and security fixes. Amazon offers instance sizes from the tiny instance available on the free-tier (which provides 5 GB of data storage, enough for sandbox and proof-of-concept projects) to sizes suitable for large data warehousing, such as their xxx. Auto-scaling is also available for mission critical and high-availibity databases with variable useage patterns.

Of course, none of this is free: a moderately-sized MySQL instance costs xx per instance hour, rounded to the nearest hour. Full-time availability for this instance runs xxx. In addition, while Amazon does not charge for automated backups or patching, these do require additional storage and usage. Database replication, which is necessary for high-availibity, requires multiple instances to be provisioned across more than one Availability Zone: for the instance described about, this doubles the monthly cost to xxx. Database logging and hourly snapshots require additional storage: logging, in particular, can be a surprising cash drain, as logs are by default updated for every single region Amazon services. This means that your local database, perhaps replicated in two regions for the home office and regional support, accumlates logging activity for the European Union, India, and China. And while the activity in these regions is, of course, minimal, Amazon charges for each actual write operation performed by one of their services (logging will typically use their Cloudtrail service, with logs stored in one or more S3 buckets). Fortunately, this default can be changed, although only from the Amazon CLI; and even so, sandbox projects on the free tier can quickly consume their entire monthly allocation of S3 usage within days, if not hours.

For all of this, the cloud is both the future and the here-and-now: migration is not an option, and the design of all cloud ecosystems--Amazon Web Services, Microsoft Azure, Google's Cloud Private, and other offerings--makes a full migration the only sensible (indeed, often the only possible) scenario. Clearly, now is the time to at least dip your toe into these vast waters; and configuring a standard SQL database using Amazon's RDS instance is a relatively painless way to do so at minimal cost.

To that end, this repository shows how to provision, configure, and load data into a MySQL instance hosted on Amazon's Relational Database Service (RDS). To simulate a production environment, a new VPC (Virtual Private Cloud) was configured to control network access to the database, and security groups were created and assigned to select roles for further access control. Within the database, user accounts and roles were configured to control access for read, ETL, and administrative roles.

The database itself is a protoype data warehouse with a standard star schema. The schema includes both one-to-many and many-to-many relations, and is generated for a series of SQL scripts. The data itself is a CSV file containing descriptions and statistics of 802 Pokemon (an amusing departure from the seriousness of business data). For the ETL operation, Python scripts are used to clean the data set and extract portions for data normalization. The data is loaded into the staging table with an additional script, and a stored procedure loads the data from the staging table into the normalized production tables.

## AWS Considerations

The database is hosted on an instance of Amazon's Relational Database Service (RDS) with MySQL 8 as the database engine. MySQL Workbench was primarily used to run queries, along with the MySQL client. Note that AWS itself does not provide a database query tool for any product besides their own proprietary offering, Amazon Aurora. The root database account was set during procurement, and the connection established from a local machine using the AWS endpoint. Note that this account is not the true "root": that is reserved for an AWS service account named (for this instace) rdsadmin. Without full root privileges, the CREATE TABLESPACE and SUPER grants are unavailable. The provisioned database also contains service tables used by AWS for database management: these are hidden by default, and should be left alone.

It takes several steps to establish a secure connection to any RDS instance.

1. Create a VPC (Virtual Private Cloud) to house the database
2. Configure a security group associated with this VPC
3. Create an Internet Gateway within the VPC and assign an Elastic IP Address

Once this is done, users may connect to the database at the IP address assigned to the Internet Gateway using their database credentials (i.e. the MySQL-based login and password), provided the security group allows inbound connections from their IP address range. Further network segmentation may be achieved through subnetting within the VPC and establishing network ACLs. Once connected, the user will have access to whatever resources and permissions their MySQL role allows: in other words, security of the database instance is done through the Amazon-provided VPC and security group, while security of database tables and assigned privileges are done through the MySQL client.

To provide another layer of security, an IAM role was associated with the database to restrict access to only those users allowed to assume the role. In effect, this requires a user to have AWS credentials as well as MySQL credentials. The AWS credentials are secured by a keypair and may be strengthened with two-factor authentication if desired.

## Data Preparation

The data used was a small CSV file containing statistics for 802 Pokemon. This data set was chosen to assist a friend with her curriculum in data science: her goal is to predict certain attributes, such as the Pokemon species, from features such as the Pokemon's attack strength, hit points, and speed. Creating a database and ETL process provides a more realistic environment for the typical data scientist role than simply reading a CSV file; database normalization also facillitates data analysis not easily performed by the structure of the data file: this is explored in more detail below.

Notwithstanding the small number of records, this data set posed several challenges to load into a normalized SQL database. These are:

* Each record contained several kanjii characters (i.e. Japanese characters) that could not be processed by MySQL's LOAD command. Removing these characters required writing a Python script to process the data as raw bytes before outputting a filtered file.
* Pokemon abilities for each record were recorded as a variable length array delimited by brackets (i.e. '[' and ']'). Abilities were separated within these brackets by commas, meaning the records could not be directly split on the comma. As MySQL does not have a native split() method, another Python script stripped the ability fields from the data file and output a sorted list of unique abilities: the stored procedure that loaded data from stage referenced this list to generate the ability table and correlate each Pokemon with its defined abilities.
* The relationship between Pokemon and their abilities was many-to-many: each Pokemon could posess one or more abilities, and each ability could be used by several different Pokemon. This required a crosswalk table to fully normalize the relationship.

### Represantive Data Sample

A representative sample of the unprocessed data is shown below. The large number of fields specifying the Pokemon's relative strength against different attacks (.e.g "against_fire") are truncated for readibility. The presence of kanjii can be seen in the Japanese Name field; the ability array is shown in the second field, Abilities. 

[sample data about here]

### Removal of Non-Standard Characters

To remove the kanjii characters from the data set, a Python script was written that processed the data set as raw bytes. The relevant code from this script is shown below: note the need to both convert between bytes and Unicode text and the steps taken to process the internal commas in the ability array.

[kanjii Python script about here]

### Processing Ability Array

As mentioned, each Pokemon's abilities were contained within a variable length array delimited by brackets and internally separated by commas. To fully normalize the tables required extracting these abilities to a separate table; this can't be easily done within MySQL, which has not native split() function or means to convert an array-like object like this field to an actual array (the JSON_ARRAY() family of functions do not work, as the entire "array" is enclosed in quotes and so treated as a single array element).

Instead, a Python script was used to extract the abilities and export them as a sorted, unique list that could be loaded with MySQL's standard LOAD syntax. The relevant code is shown below. It shows a helpful hack by using the set() function to quickly remove duplicate abilities; since this does not preserve the order of elements, the result is converted back into a list and sorted to create the data set to be exported.

[ability Python script about here]

An additional Python script was used to extract the Pokemon type field for database normalization: this can be viewed, along with the other Python scripts, in the Scripts folder. As it contains no code that is significantly different from that shown here, it is ommitted for space considerations.

## Database Definition

The database is named pokemon and generated via SQL scripts. There are 5 tables; one of these is the staging table, which loads the data unaltered, while the remaining tables are normalized for production. The schema below was generated with xxx and illustrates the table relationships: note that as with the data sample, some fields in the statistics table are ommitted for clarity.

[schema def about here]

### Table Definitions

All tables were defined using standard SQL syntax. The abilities, species, and statistics tables are straightforward and not shown here. The definition of the crosswalk table, statistics_to_abilities_xwalk, is potentially more interesting and  shown below,

[crosswalk tabledef about here]

The table has two columns, both foreign keys to the ability and statistics table. For each record in the statistics table, the record id (pokemon_id) is related to the ability_ids corresponding to the set of abilities in the ability table that the Pokemon may use. An example of this relationship is shown below for the Pokemon named Bulbasaur. This Pokemon has two abilities, xxx and xxx, corresponding to two entries in the crosswalk table. Its pokemon_id from the statistics table is related to the ability_ids for these abilities, so that the crosswalk table has two rows for this Pokemon.

[example xwalk for a single Pokemon about here]

The next figure shows the SQL query that recovers this relationship into a single recordset: note that the Pokemon's name (and in fact any fields from the statistics table included in the query) appears twice. This results from the definition of the crosswalk table, which has one entry for *each* ability the Pokemon may use. If this behavior is not desired, the abilities may be serialized using the JSON_ARRAY() set of functions, with the resultant query used to define a View for easy access.

[SQL query to join statistics, abilities, and xwalk about here]

### Stored Procedures

To transfer the staging data to the normalized tables, the stored procedure load_data_from_stage was written. This procedure used a cursor to insert each row of data from the staging table into the statistics table. The procedure then retrieved the last inserted ID and inserted it, along with the ability IDs of the abilities the Pokemon could use, into the crosswalk table. Because the abilities in the staging table were stored in a pseudo-array, the procedure used the INSTR() function on the abilities field to determine the appropriate abilities for each row, and then selected the ability_ID from the abilities table corresponding to the selected values. This generated each set of entries into the crosswalk table without needing to split the abilities field in the staging table into individual elements. The code that performed this operation is shown below.

[cursor code to insert Pokemon into statistics table]

Since the species field was normalized as a separate table, the cursor also inserted the appropriate species_id into the statistics table by selecting the species_ID from the species table corresponding to the Pokemon's species in the staging table (where the field is named type1). The relevant code for this operation is shown below.

## Summary

This project created a normalized database from a small data set describing Pokemon abilities and statistics. The normalized schema contains four tables: the primary data table statistics, which functions as the fact table; the dimension table species; the dimension table abilities; and the crosswalk table linking the statistics data to the abilities table. The fact table contains 802 rows, each representing a distinct Pokemon. The normalized schema allows a wide range of queries to be performed, including queries not easily performed against the raw data set, such as retrieving the Pokemon able to use each ability. Useful queries may easily be stored as views, and the statistics table may be further normalized by creating new relationship tables for the remaining feature dimensions.

The database itself is provided as in instance of Amazon's Relational Database Service. Securing access required both networking and policy services (i.e. the Virtual Private Cloud and Identity and Access Management services) as well as database-specific roles and permissions. Security groups were also established, and keypairs generated for programmatic access via the RDS SDK and Amazon CLI.

While the database itself is relatively small, the steps outlined here may easily be used to manage access to much larger data sets suitable for a SQL environment. For such data sets, indices and partitioning may easily be performed to minimize query time. Hopefully, the brief discussion presented here will encourage people to try Amazon's RDS service for similar projects.
