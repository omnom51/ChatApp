import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ChatService } from './chat.service';
import { AuthService } from '../auth.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [CommonModule, FormsModule, MatInputModule, MatButtonModule],
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.css']
})
export class ChatComponent implements OnInit {
  messages: any[] = [];
  content: string = '';
  username: string = '';

  constructor(
    private chatService: ChatService,
    private authService: AuthService,
    private router: Router
  ) {}

  ngOnInit(): void {
    const token = this.authService.getToken();
    if (!token) {
      console.error('Token not found, redirecting to login');
      this.router.navigate(['/login']);
      return;
    }

    this.username = token;
    this.chatService.connect();
    this.chatService.getMessages().subscribe((message: any) => {
      this.messages.push(JSON.parse(message));
    });
    this.chatService.getAllMessages().subscribe((messages: any) => {
      this.messages = messages;
    });
  }

  sendMessage() {
    this.chatService.sendMessage(this.content, this.username);
    this.content = '';
  }

  logout() {
    this.authService.logout();
  }
}
