import React, { useState } from 'react';
import { 
  Container, 
  Paper, 
  Button, 
  Typography, 
  Box,
  List,
  ListItem,
  ListItemText,
  CircularProgress
} from '@mui/material';

function App() {
  console.log("********** hyundai1 **********");
  const [messages, setMessages] = useState([]);
  const [buttons, setButtons] = useState(['차량 정보', '자주 묻는 질문', '상담원 연결']);
  const [loading, setLoading] = useState(false);
  const BACKEND_URL = 'https://hyundai-chatbot-backend.onrender.com';
  // 메시지 전송 함수
  const sendMessage = async (content) => {
    try {
      setLoading(true);
      // 사용자 메시지 추가
      console.log("********** hyundai2 **********");
      setMessages(prev => [...prev, { text: content, sender: 'user' }]);

      // 서버에 메시지 전송
      console.log("********** hyundai3 **********");
      const response = await fetch(`${BACKEND_URL}/message`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'Origin': 'https://hyundai-chatbot.vercel.app'
        },
        mode: 'cors',
        credentials: 'omit',
        body: JSON.stringify({ content })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      // JSON 응답 파싱
      const data = await response.json();

      // 봇 응답 추가
      if (data && data.message) {
        setMessages(prev => [...prev, { 
          text: data.message.text, 
          sender: 'bot' 
        }]);

        // 버튼 업데이트
        if (data.keyboard && data.keyboard.buttons) {
          setButtons(data.keyboard.buttons);
        }
      } else {
        throw new Error('Invalid response format');
      }
    } catch (error) {
      console.error('Error:', error);
      let errorMessage = '죄송합니다. 오류가 발생했습니다.';
      
      if (error.code === 'ECONNREFUSED') {
        errorMessage = '서버에 연결할 수 없습니다. 서버가 실행 중인지 확인해주세요.';
      } else if (error.code === 'ETIMEDOUT') {
        errorMessage = '서버 응답 시간이 초과되었습니다. 다시 시도해주세요.';
      }
      
      setMessages(prev => [...prev, { 
        text: errorMessage, 
        sender: 'bot' 
      }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="sm" sx={{ mt: 4 }}>
      <Typography variant="h4" gutterBottom align="center">
        현대자동차 챗봇
      </Typography>
      
      {/* 메시지 목록 */}
      <Paper 
        elevation={3} 
        sx={{ 
          height: '60vh', 
          overflow: 'auto', 
          p: 2, 
          mb: 2,
          backgroundColor: '#f5f5f5'
        }}
      >
        <List>
          {messages.map((message, index) => (
            <ListItem 
              key={index}
              sx={{ 
                justifyContent: message.sender === 'user' ? 'flex-end' : 'flex-start'
              }}
            >
              <Paper 
                elevation={1}
                sx={{
                  p: 1,
                  maxWidth: '70%',
                  backgroundColor: message.sender === 'user' ? '#e3f2fd' : 'white'
                }}
              >
                <ListItemText 
                  primary={message.text}
                  sx={{ 
                    wordBreak: 'break-word'
                  }}
                />
              </Paper>
            </ListItem>
          ))}
          {loading && (
            <ListItem sx={{ justifyContent: 'center' }}>
              <CircularProgress size={24} />
            </ListItem>
          )}
        </List>
      </Paper>

      {/* 버튼 그룹 */}
      <Box 
        sx={{ 
          display: 'flex', 
          flexWrap: 'wrap', 
          gap: 1, 
          justifyContent: 'center'
        }}
      >
        {buttons.map((button, index) => (
          <Button
            key={index}
            variant="contained"
            onClick={() => sendMessage(button)}
            disabled={loading}
            sx={{ 
              backgroundColor: '#002c5f',
              '&:hover': {
                backgroundColor: '#00205f'
              }
            }}
          >
            {button}
          </Button>
        ))}
      </Box>
    </Container>
  );
}

export default App;
