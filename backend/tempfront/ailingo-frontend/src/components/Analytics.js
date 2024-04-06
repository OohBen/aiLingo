import React, { useEffect, useState } from 'react';
import { Container, Row, Col, Card } from 'react-bootstrap';
import { Bar } from 'react-chartjs-2';
import axiosInstance from '../utils/axiosInstance';
import { Chart, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';
Chart.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

function Analytics() {
  const [analyticsData, setAnalyticsData] = useState(null);

  useEffect(() => {
    fetchAnalyticsData();
  }, []);

  const fetchAnalyticsData = async () => {
    try {
      const response = await axiosInstance.get('/analytics/user-analytics/');
      setAnalyticsData(response.data);
    } catch (error) {
      console.error('Error fetching analytics data:', error);
    }
  };

  const renderCharts = () => {
    if (!analyticsData) return null;

    const languageProgressData = {
      labels: Object.keys(analyticsData.language_progress),
      datasets: [
        {
          label: 'Completion Percentage',
          data: Object.values(analyticsData.language_progress).map(
            (progress) => progress.completion_percentage
          ),
          backgroundColor: 'rgba(75, 192, 192, 0.6)',
        },
      ],
    };

    const quizAnalyticsData = {
      labels: Object.keys(analyticsData.quiz_analytics),
      datasets: [
        {
          label: 'Total Quizzes',
          data: Object.values(analyticsData.quiz_analytics).map(
            (analytics) => analytics.total_quizzes
          ),
          backgroundColor: 'rgba(75, 192, 192, 0.6)',
        },
      ],
    };

    const chatAnalyticsData = {
      labels: Object.keys(analyticsData.chat_analytics),
      datasets: [
        {
          label: 'Total Chats',
          data: Object.values(analyticsData.chat_analytics).map(
            (analytics) => analytics.total_chats
          ),
          backgroundColor: 'rgba(75, 192, 192, 0.6)',
        },
      ],
    };

    const options = {
      scales: {
        x: {
          title: {
            display: true,
            text: 'Languages',
          },
        },
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: 'Value',
          },
        },
      },
    };

    return (
      <>
        <Row>
          <Col>
            <Card>
              <Card.Body>
                <Card.Title>Language Progress</Card.Title>
                <Bar data={languageProgressData} options={{ ...options, scales: { ...options.scales, y: { ...options.scales.y, title: { ...options.scales.y.title, text: 'Completion Percentage' } } } }} />
              </Card.Body>
            </Card>
          </Col>
        </Row>
        <Row>
          <Col>
            <Card>
              <Card.Body>
                <Card.Title>Quiz Analytics</Card.Title>
                <Bar data={quizAnalyticsData} options={{ ...options, scales: { ...options.scales, y: { ...options.scales.y, title: { ...options.scales.y.title, text: 'Total Quizzes' } } } }} />
              </Card.Body>
            </Card>
          </Col>
        </Row>
        <Row>
          <Col>
            <Card>
              <Card.Body>
                <Card.Title>Chat Analytics</Card.Title>
                <Bar data={chatAnalyticsData} options={{ ...options, scales: { ...options.scales, y: { ...options.scales.y, title: { ...options.scales.y.title, text: 'Total Chats' } } } }} />
              </Card.Body>
            </Card>
          </Col>
        </Row>
      </>
    );
  };

  return (
    <Container>
      <h1>Analytics</h1>
      {analyticsData ? renderCharts() : <p>Loading analytics data...</p>}
    </Container>
  );
}

export default Analytics;