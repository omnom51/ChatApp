import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, Subject } from 'rxjs';
import SockJS from 'sockjs-client';
import { Stomp } from '@stomp/stompjs';
import { AuthService } from '../auth.service';

@Injectable({
  providedIn: 'root'
})
export class ChatService {
  private stompClient: any;
  private messageSubject: Subject<string> = new Subject<string>();
  private readonly apiUrl = 'http://localhost:8080/api/chat';

  constructor(private authService: AuthService, private http: HttpClient) {}

  connect() {
    const socket = new SockJS('http://localhost:8080/chat');
    this.stompClient = Stomp.over(socket);

    this.stompClient.connect({}, () => {
      this.stompClient.subscribe('/topic/messages', (message: any) => {
        if (message.body) {
          this.messageSubject.next(message.body);
        }
      });
    });
  }

  sendMessage(content: string, username: string) {
    const token = this.authService.getToken();
    this.stompClient.send('/app/send', {}, JSON.stringify({ content, username, token }));
  }

  getMessages(): Observable<string> {
    return this.messageSubject.asObservable();
  }

  getAllMessages() {
    return this.http.get(`${this.apiUrl}/messages`);
  }
}
