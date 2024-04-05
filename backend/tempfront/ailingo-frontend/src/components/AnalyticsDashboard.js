import React, { useEffect, useState } from 'react';
import { Container, Row, Col, Card } from 'react-bootstrap';
import { Bar } from 'react-chartjs-2';
import axiosInstance from '../utils/axiosInstance';

function AnalyticsDashboard() {
  const [analyticsData, setAnalyticsData] = useState(null);

  useEffect(() => {
    fetchAnalyticsData();
  }, []);

  const fetchAnalyticsData = async () => {
    try {
      const response = await axiosInstance.get('/analytics/');
      setAnalyticsData(response.data);
    } catch (error) {
      console.error('Error fetching analytics data:', error);
    }
  };

  if (!analyticsData) {
    return <div>Loading...</div>;
  }

  const { metrics } = analyticsData.data;

  const chartData = {
    labels: metrics.map((metric, index) => `Metric ${index + 1}`),
    datasets: [
      {
        label: 'Analytics',
        data: metrics.map((metric) => parseFloat(metric.split(':')[1])),
        backgroundColor: 'rgba(75, 192, 192, 0.6)',
      },
    ],
  };

  return (
    <Container>
      <h1>Analytics Dashboard</h1>
      <Row>
        <Col>
          <Card>
            <Card.Body>
              <Bar data={chartData} />
            </Card.Body>
          </Card>
        </Col>
      </Row>
      <Row>
        {metrics.map((metric, index) => (
          <Col key={index} md={4}>
            <Card>
              <Card.Body>
                <Card.Title>{metric.split(':')[0]}</Card.Title>
                <Card.Text>{metric.split(':')[1]}</Card.Text>
              </Card.Body>
            </Card>
          </Col>
        ))}
      </Row>
    </Container>
  );
}

export default AnalyticsDashboard;