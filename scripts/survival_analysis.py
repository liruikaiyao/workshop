from lifelines.datasets import generate_regression_dataset
regression_dataset = generate_regression_dataset()
from lifelines import AalenAdditiveFitter, CoxPHFitter
cf = CoxPHFitter()
cf.fit(regression_dataset, duration_col='T', event_col='E')
aaf = AalenAdditiveFitter(fit_intercept=False)
aaf.fit(regression_dataset, duration_col='T', event_col='E')
x = regression_dataset[regression_dataset.columns - ['E','T']]
aaf.predict_survival_function(x.ix[10:12]).plot()
aaf.plot()
