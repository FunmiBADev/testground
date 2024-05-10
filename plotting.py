import pandas as pd
import matplotlib.pyplot as plt

# Assuming selected_columns is your DataFrame

# Scatter Plot
plt.figure(figsize=(10, 6))
plt.scatter(selected_columns['name'], selected_columns['jre'])
plt.title('Scatter Plot of Name vs JRE')
plt.xlabel('Name')
plt.ylabel('JRE')
plt.xticks(rotation=45, ha='right')  # Rotating x-axis labels for better readability
plt.tight_layout()  # Adjust layout to prevent clipping of labels
plt.show()


import pandas as pd
import matplotlib.pyplot as plt

# Assuming selected_columns is your DataFrame

# Grouping by 'name' and aggregating 'jre' values
grouped_data = selected_columns.groupby('name')['jre'].value_counts().unstack(fill_value=0)

# Bar Graph
plt.figure(figsize=(12, 6))
grouped_data.plot(kind='bar', stacked=True)
plt.title('Bar Plot of JRE by Name')
plt.xlabel('Name')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')
plt.legend(title='JRE')
plt.tight_layout()
plt.show()

import pandas as pd
import matplotlib.pyplot as plt

# Assuming selected_columns is your DataFrame

# Grouping by 'name' and 'jre' and counting occurrences
grouped_data = selected_columns.groupby(['name', 'jre']).size().unstack(fill_value=0)

# Grouped Bar Plotting
plt.figure(figsize=(12, 6))
grouped_data.plot(kind='bar')
plt.title('Grouped Bar Plot of JRE by Name')
plt.xlabel('Name')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')
plt.legend(title='JRE')
plt.tight_layout()
plt.show()

import pandas as pd
import matplotlib.pyplot as plt

# Assuming selected_columns is your DataFrame

# Calculating the frequency of each 'jre' value
jre_counts = selected_columns['jre'].value_counts()

# Pie Chart
plt.figure(figsize=(8, 8))
plt.pie(jre_counts, labels=jre_counts.index, autopct='%1.1f%%', startangle=140)
plt.title('Distribution of JRE Values')
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
plt.show()

