# ETL to AWS RDS MySQL Instance

This project demonstrates at ETL process using a small data set and a MySQL instance hosted on Amazon's Relational Database Service (RDS). Python scripts are used to clean the data set and extract portions for data normalization. The database and tables are then created with several SQL scripts and the data loaded with additional scripts. A stored procedure loads the data from the staging table into the normalized production tables.

The database itself is hosted on Amazon Web Services (AWS) with their RDS service; to simulate a more realistic production environment, a new VPC (Virtual Private Cloud) was configured to control network access to the database, and security groups were created and assigned to select roles for further access control. Within the database, user accounts and roles were configured to control access for read, ETL, and administrative roles.

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

Indices were created for the pokemon_name field on the statistics table, as well as the ability_type and species_type fields on those respective tables. Non-null and check constraints were also added to each table to ensure data integrity; a description of each may be found in the relative table definition.

### User Roles

Three user roles were established in addition to the admin (pseudo-root) account added during RDS configuration. These are standard roles for a small database, and provide a means to segment user access to only those objects and permissions needed.

* database_admin
* etl_user
* query_user

The database_admin role had all available permissions on the database (but only this database). The etl_user may perform CRUD operations and may also create temporary tables and execute stored procedures. The query_user may query all tables except for the stage table. They may also export data from these tables if so desired.
