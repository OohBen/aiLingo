import React, { useEffect, useState } from 'react';
import { Container, Row, Col, Card } from 'react-bootstrap';
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

  return (
    <Container>
      <h1>Analytics</h1>
      <Row>
        <Col>
          <Card>
            <Card.Body>
              <Card.Title>User Analytics</Card.Title>
              {analyticsData && (
                <div>
                  <p>{analyticsData.data}</p>
                </div>
              )}
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
}

export default Analytics;