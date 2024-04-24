from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.metrics import r2_score
from mpl_toolkits.mplot3d import Axes3D

df = pd.read_excel('Data_files_Pysentiment_FFR.xlsx', 'Input')

# Extracting variables from excel
TwoYear_yields = df['2Y_Yields']
Sentiment_score = df['Score_(EOM)']
PCE_yoy = df['PCE']

# No lag (sentiment vs. 2y yields)
plt.scatter(Sentiment_score, TwoYear_yields)
z = np.polyfit(Sentiment_score, TwoYear_yields, 1)
p = np.poly1d(z)
plt.xlabel('Sentiment scores')
plt.ylabel('2Y yields')
plt.plot(Sentiment_score,p(Sentiment_score))
print(r2_score(TwoYear_yields, p(Sentiment_score)))

# correlation_matrix = np.corrcoef(Sentiment_score, TwoYear_yields)
# correlation_xy = correlation_matrix[0,1]
# print(correlation_xy**2)

# No lag (sentiment & pce vs. 2y yields)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(Sentiment_score, PCE_yoy, TwoYear_yields)

# Fit a plane using np.linalg.lstsq
A = np.vstack([Sentiment_score,PCE_yoy,np.ones_like(Sentiment_score)]).T
plane_coef, _, _, _ = np.linalg.lstsq(A, TwoYear_yields, rcond=None)

# Create a meshgrid for the plane
x_plane, y_plane = np.meshgrid(Sentiment_score, PCE_yoy)
z_plane = plane_coef[0] * x_plane + plane_coef[1] * y_plane + plane_coef[2]

# Add the regression plane
surfacePlot = ax.plot_surface(x_plane, y_plane, z_plane, cmap='viridis', \
            alpha = 0.7, linewidth=0, antialiased=True, shade=True)
#fig.colorbar(surfacePlot, orientation='horizontal')

# fig.colorbar(ax.plot_surface(x_plane, y_plane, z_plane), shrink=0.5, aspect=5) 

# Add labels and title
ax.set_xlabel('Sentiment scores')
ax.set_ylabel('PCE yoy')
ax.set_zlabel('2Y yields')
ax.zaxis.labelpad = -3.5
#plt.title('Multivariate Regression')
plt.show()

# Compute r^2 for multivariate regression
model = LinearRegression()
X, y = df[['Score_(EOM)', 'PCE']], df['2Y_Yields']
model.fit(X ,y)
print(model.score(X, y))








