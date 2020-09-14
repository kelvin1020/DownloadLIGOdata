from gwpy.timeseries import TimeSeries
data = TimeSeries.fetch_open_data('L1', 968654552, 968654562, verbose = True, cache = True)

plot = data.plot(
    title='LIGO Livingston Observatory data for HW100916',
    ylabel='Strain amplitude',
)
plot.show()