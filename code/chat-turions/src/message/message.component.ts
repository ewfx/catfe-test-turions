import { Component } from '@angular/core';
import { ChatService } from '../app/chat.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
interface Message {
  sender: 'You' | 'Me';
  text: string;
}
@Component({
  selector: 'app-message',
  imports: [CommonModule, FormsModule],
  templateUrl: './message.component.html',
  styleUrl: './message.component.css'
})
export class MessageComponent {
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
