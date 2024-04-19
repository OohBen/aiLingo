import { Analytics } from '../types';
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

type AnalyticsChartProps = {
  data: Analytics;
};

export function AnalyticsChart({ data }: AnalyticsChartProps) {
  const chartData = {
    labels: Object.keys(data),
    datasets: [
      {
        label: 'Analytics',
        data: Object.values(data),
        backgroundColor: 'rgba(75, 192, 192, 0.6)',
      },
    ],
  };

  const options = {
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  };

  return (
    <div className="bg-white shadow-md rounded-lg p-4">
      <h2 className="text-xl font-semibold mb-4">Analytics</h2>
      <Bar data={chartData} options={options} />
    </div>
  );
}