<h1 align='center'>python-discord-data-bot<h1>
This is a Python script that retrieves the number of downloads of a GNOME extension called "Disk Usage" from the GNOME Extensions website and stores the data in a local file. It also creates a bar graph that shows the total number of downloads per day and sends it to a Discord channel upon request.

The script uses the requests and lxml libraries to extract the download count from the website, and the discord and matplotlib libraries to send the graph to Discord and generate the graph respectively. It also uses a configuration file to store sensitive information, such as the Discord bot token.

The script checks the local file for existing data and updates it if the current date and content are already in the file or adds new data if the current date is not in the file. The script also prevents duplicate content on the same line in the local file.

The script responds to various Discord messages, such as "graph" to generate and send the graph, "data" or "Data" to retrieve the current number of downloads, "shutdown" to stop the script, and "WhoAmI" to show the user's name in the channel.
