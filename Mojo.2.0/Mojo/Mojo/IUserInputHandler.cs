﻿using System.Windows.Input;

namespace Mojo
{
    public interface IUserInputHandler
    {
        void OnKeyDown(KeyEventArgs keyEventArgs, int width, int height);
        void OnKeyUp(KeyEventArgs keyEventArgs, int width, int height);

        void OnMouseDown( System.Windows.Forms.MouseEventArgs mouseEventArgs, int width, int height );
        void OnMouseUp( System.Windows.Forms.MouseEventArgs mouseEventArgs, int width, int height );
        void OnMouseClick( System.Windows.Forms.MouseEventArgs mouseEventArgs, int width, int height );
        void OnMouseDoubleClick( System.Windows.Forms.MouseEventArgs mouseEventArgs, int width, int height );
        void OnMouseMove( System.Windows.Forms.MouseEventArgs mouseEventArgs, int width, int height );
        void OnMouseWheel( System.Windows.Forms.MouseEventArgs mouseEventArgs, int width, int height );

        void OnManipulationDelta( ManipulationDeltaEventArgs manipulationEventArgs, int width, int height );

        void SetSize( int oldWidth, int oldHeight, int newWidth, int newHeight );
    }
}
