"use strict";
(function(window, $, undefined) {

var Zero = {

    statics: {
        sector: {
            'tc': 'Telecommunications Services',
            'in': 'Industrials',
            'cd': 'Consumer Discretionary',
            'ut': 'Utilities',
            'cs': 'Consumer Staples',
            'hc': 'Health Care',
            'ma': 'Materials',
            'fi': 'Financials',
            'en': 'Energy',
            'it': 'Information Technology'
        }
    },

    number_class: function(num) {
        if (num > 0) { return 'pos'; }
        if (num < 0) { return 'neg'; }
        return 'neu';
    },

    api: function(params) {
        $.ajax({
            url: params.url,
            data: params.data,
            dataType: 'json',
            success: function(data, textStatus, jqXHR) {
                params.callback(data);
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.log(textStatus);
                console.log(errorThrown);
            }
        });
    },

    sector: function(key) {
        return (key in this.statics.sector) ? this.statics.sector[key] : '';
    },

    ohlc_stats: function(data) {
        var stats = { high: 0, low: 1000000000, current: 0, oldest: 0, ohlc: [] };
        for (var i = 0, il = data.length; i < il; i++) {
            var line = { date: new Date(data[i][0] * 1000), open: data[i][1], high: data[i][2], low: data[i][3], close: data[i][4] };
            stats.ohlc.push(line);
            if (line.close > stats.high) { stats.high = line.close; }
            if (line.close < stats.low) { stats.low = line.close; }
        }
        stats.oldest            = stats.ohlc[0].close;
        stats.current           = stats.ohlc[stats.ohlc.length-1].close;
        stats.high_diff         = parseFloat((stats.high - stats.current).toFixed(2));
        stats.low_diff          = parseFloat((stats.low - stats.current).toFixed(2));
        stats.high_diff_pct     = parseFloat(((stats.high_diff / stats.current) * 100).toFixed(1));
        stats.low_diff_pct      = parseFloat(((stats.low_diff / stats.current) * 100).toFixed(1));
        stats.oldest_diff       = parseFloat((stats.current - stats.oldest).toFixed(2));
        stats.oldest_diff_pct   = parseFloat(((stats.oldest_diff / stats.current) * 100).toFixed(1));
        if (stats.low === 1000000000) { stats.low = 0; }
        return stats;
    }

};

window.Zero = Zero;

})(window, jQuery);
