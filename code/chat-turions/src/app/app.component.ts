import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterOutlet } from '@angular/router';
import { ChatService } from './chat.service';

interface Message {
  sender: 'You' | 'Me';
  text: string;
}

@Component({
  selector: 'app-root',
  imports: [CommonModule, FormsModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'chat-turions';
  messages: { text: string; isUser: boolean }[] = [];
  userInput: string = '';
  constructor(private chatService: ChatService) {}
  sendMessage() {
    if (this.userInput.trim() === '') return;

    // Add user message
    this.messages.push({ text: this.userInput, isUser: true });

    this.chatService.sendMessage(this.userInput).subscribe(
      (response) => {
        const botMessage = { text: response.response, isUser: false };
        this.messages.push(botMessage);
      },
      (error) => {
        console.error('Error sending message:', error);
        this.messages.push({ text: 'Error communicating with server', isUser: false });
      }
    );
    
    // Simulate bot response
    setTimeout(() => {
      this.messages.push({ text: this.getBotResponse(this.userInput), isUser: false });
    }, 1000);

    this.userInput = '';
  }

  getBotResponse(userMessage: string): string {
    const responses: { [key: string]: string } = {
      'hello': 'Hi there! How can I help you?',
      'how are you': 'I am just a bot, but I am doing great!',
      'bye': 'Goodbye! Have a nice day!',
    };

    return responses[userMessage.toLowerCase()] || "I'm not sure how to respond to that.";
  }
}
