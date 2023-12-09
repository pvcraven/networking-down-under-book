import java.awt.event.*;
import java.awt.Graphics;
import java.awt.Color;
import java.util.ArrayList;
import java.util.List;
import javax.swing.JPanel;
import javax.swing.JFrame;
import javax.swing.Timer;
import java.util.Random;

public class BouncingBall
{
    // execute application
    public static void main( String args[] ) {
        JFrame frame = new JFrame("Bouncing Ball");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        BallPanel ballPanel = new BallPanel();
        frame.add(ballPanel);
        frame.setSize(800, 600); // set frame size
        frame.setVisible(true); // display frame

        frame.addKeyListener(new KeyListener() {
            @Override
            public void keyTyped(KeyEvent e) {
            }

            @Override
            public void keyPressed(KeyEvent e) {
                if(e.getKeyCode() == ' ') {
                    ballPanel.addBall();
                }
            }

            @Override
            public void keyReleased(KeyEvent e) {
            }
        });

    }
}

class Ball
{
    Color col;
    int x = 0;		// x position
    int y = 0;		// y position
    int dx = 0;		// increment amount (x coord)
    int dy = 0;		// increment amount (y coord)
    int radius = 15;	// ball radius
}

class BallPanel extends JPanel implements ActionListener
{
    private List <Ball> ballList = new ArrayList();
    private Random rand = new Random();

    public BallPanel()
    {
        int delay = 10;
        Timer timer;
        timer = new Timer(delay, this);
        timer.start();		// start the timer
    }

    public void addBall()
    {
        Ball ball = new Ball();
        ball.x = rand.nextInt(getWidth());
        ball.y = rand.nextInt(getHeight());
        while(ball.dx == 0 && ball.dy == 0) {
            ball.dx = rand.nextInt(11) - 5;
            ball.dy = rand.nextInt(11) - 5;
        }
        ball.radius = rand.nextInt(20) + 20;
        int red = rand.nextInt(256);
        int green = rand.nextInt(256);
        int blue = rand.nextInt(256);
        ball.col = new Color(red, green, blue);
        ballList.add(ball);
    }
    public void actionPerformed(ActionEvent e)
    {
        repaint();
    }

    // draw rectangles and arcs
    public void paintComponent( Graphics g )
    {
        super.paintComponent(g); // call superclass's paintComponent

        for(Ball ball : ballList) {
            g.setColor(ball.col);

            // check for boundaries
            if (ball.x < ball.radius)
            {
                ball.dx = Math.abs(ball.dx);
            }

            if (ball.x > getWidth() - ball.radius)
            {
                ball.dx = -Math.abs(ball.dx);
            }

            if (ball.y < ball.radius)
            {
                ball.dy = Math.abs(ball.dy);
            }

            if (ball.y > getHeight() - ball.radius)
            {
                ball.dy = -Math.abs(ball.dy);
            }

            // adjust ball position
            ball.x += ball.dx;
            ball.y += ball.dy;
            g.fillOval(ball.x - ball.radius, ball.y - ball.radius, ball.radius*2, ball.radius*2);
        }

    }

}