import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { ContentComponent } from './content/content.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    RouterOutlet,
    ContentComponent
  ],
  template: `
    <main class="main">
      <h1>Fiesta!</h1>
      <div class="content">
        <app-content></app-content>
      </div>
    </main>
  `,
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'fiesta';

}
