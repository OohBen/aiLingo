// Analytics.js

import React, { useEffect, useState } from 'react';
import { Container, Row, Col, Card } from 'react-bootstrap';
import { Line } from 'react-chartjs-2';
import axiosInstance from '../utils/axiosInstance';

function Analytics() {
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

  const renderChart = () => {
    if (!analyticsData) return null;

    const chartData = {
      labels: Object.keys(analyticsData.data),
      datasets: [
        {
          label: 'Analytics',
          data: Object.values(analyticsData.data),
          fill: false,
          borderColor: 'rgb(75, 192, 192)',
          tension: 0.1,
        },
      ],
    };

    return <Line data={chartData} />;
  };

  return (
    <Container>
      <h1>Analytics</h1>
      <Row>
        <Col>
          <Card>
            <Card.Body>
              <Card.Title>User Analytics</Card.Title>
              {analyticsData ? (
                <>
                  <p>Total Quizzes: {analyticsData.total_quizzes}</p>
                  <p>Average Score: {analyticsData.average_score.toFixed(2)}%</p>
                  {renderChart()}
                </>
              ) : (
                <p>Loading analytics data...</p>
              )}
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
}

export default Analytics;