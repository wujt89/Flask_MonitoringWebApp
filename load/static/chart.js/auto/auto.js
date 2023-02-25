import {Chart, registerables} from 'chart.js/dist/chart';

Chart.register(...registerables);

export * from 'chart.js/dist/chart';
export default Chart;
