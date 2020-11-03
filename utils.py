import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False


def plot(df, col, size=10, show_data=True):
	# barchart
	items = []
	for i, j in df[col].value_counts().items():
		if i not in [r"\N", "--", "", "nan"]:
			items.append((i, j))

	try:
		items = sorted(items, key=lambda x: int(re.sub("[^0-9]", "", x[0])))
	except:
		pass

	order = [i[0] for i in items]
	plt.figure(figsize=(size, 5))
	sns.set(style="darkgrid", )
	g = sns.countplot(x=col, data=df, order=order, )

	if show_data:
		for i, j in items:
			g.text(order.index(i), j, j, color="black", ha="center")

	plt.xticks(rotation=70)
	plt.show()


def box(df, cols=[], size=25):
	# boxplot
	plt.figure(figsize=(size, 5))
	sns.set(style="darkgrid", )
	temp_df = df.copy(deep=True)

	for i in range(len(cols)):
		x = int(f"1{len(cols)}{i+1}")
		ax = plt.subplot(x)
		temp_df[cols[i]] = temp_df[cols[i]].map(lambda x: int(x) if re.search('[0-9]', str(x)) else np.nan)
		sns.boxplot(y=cols[i], data=temp_df, ax=ax)
	plt.show()


def line(df, fes=[], size=250, hline=False):
	# lineplot
	plt.figure(figsize=(25, size))
	sns.set(style="darkgrid")
	temp_df = df.copy(deef=True)

	for i in range(len(fes)):
		ax = plt.subplot(len(fes), 2, i+1)
		if hline:
			ax.axhline(y=0.1, color='green', linestyle='--')
			ax.axhline(y=0.25, color='green', linestyle='--')
		else:
			ax.set_ylim((-0.1, 1,1))
		sns.lineplot(x='index', y=fes[i], data=temp_df, ax=ax, sort=False)
	plt.show()


def split_df(df, split_col):
	# split dataframe
	records = df.to_dict('record')
	final_ret = []
	for rec in records:
		splits = rec[split_col]
		if isinstance(splits, list):
			ret = [{**rec, **split} for split in splits]
		else:
			ret = [rec]
		final_ret += ret
	df_ret = pd.DataFrame(final_ret)
	del df_ret[split_col]
	return df_ret


def coverage_calc(df, colnames=None, mi_values=[], mi_dict={}):
	result = []
	if not colnames:
		colnames = df.columns.tolist()
	for name in colnames:
		try:
			new_mi_values = set(mi_values + mi_dict.get(name, []))
		except:
			new_mi_values = set(mi_values + [mi_dict[name]])
		mi_item_total = df[name].isnull().sum() + df[name].isin(new_mi_values).sum()
		mi_perc = mi_item_total / len(df[name])
		name_coverage = 1 - mi_perc
		result.append(name_coverage)

	output = pd.DataFrame({"feature_name": colnames, "coverage": result})
	output = output.sort_values("coverage", ascending=False)
	output = output.reset_index().drop("index", axis=1)
	return output[["feature_name", "coverage"]]